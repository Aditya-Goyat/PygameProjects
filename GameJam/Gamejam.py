import pygame, sys
import math
import random

from pygame.constants import K_SPACE, K_a, K_d

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Circle.png")
        self.rect = self.image.get_rect(center = (200,700))
        self.speed = 4

    def player_move(self):
        keys = pygame.key.get_pressed()
        if keys[K_d]:
                self.rect.x += self.speed
        elif keys[K_a]:
                self.rect.x -= self.speed
    
    def player_restriction(self):
        if self.rect.right >= 450:
            self.rect.right = 450
        if self.rect.left <= 0:
            self.rect.left = 0

    def update(self):
        self.player_restriction()
        self.player_move()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, targetx, targety):
        super().__init__()
        self.image = pygame.image.load("Bullet.png")
        self.rect = self.image.get_rect(center = pos)
        x = pos[0]
        y = pos[1]
        angle = math.atan2(targety-y, targetx-x)
        self.dx = math.cos(angle)*9
        self.dy = math.sin(angle)*9
        self.x = x
        self.y = y
        self.tolerance = 10
        Bullet.rebound = False
        self.bulletbounce = pygame.mixer.Sound("mixkit-game-ball-tap-2073.wav")

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.rect.top <= 0:
            self.dy *= -1
            Bullet.rebound = True
            self.bulletbounce.play()
        if self.rect.right >= 450:
            self.dx *= -1
            self.bulletbounce.play()
        if self.rect.left <= 0:
            self.dx *= -1
            self.bulletbounce.play()

    def collision(self):
        if game.mat:
            for mats in game.mat:
                    if self.rect.colliderect(mats.rect):
                        if abs(mats.rect.bottom - self.rect.top) < self.tolerance:
                            self.dy *= -1
                            Bullet.rebound = True
                            self.bulletbounce.play()
                        if abs(mats.rect.top - self.rect.bottom) < self.tolerance:
                            self.dy *= -1
                            Bullet.rebound = True
                            self.bulletbounce.play()
                        if abs(self.rect.right - self.rect.left) < self.tolerance:
                            self.dx *= -1
                            self.bulletbounce.play()
                        if abs(mats.rect.right - self.rect.left) < self.tolerance:
                            self.dx *= -1
                            self.bulletbounce.play()

    def update(self):
        self.move()
        self.collision()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        colors = ['red', 'yellow', 'green']
        color = random.choice(colors)
        file_path = color + '.png'
        self.image= pygame.image.load(file_path)
        self.rect = self.image.get_rect(center = pos)
        self.speed = 2
    
    def move(self):
        self.rect.y += self.speed

    def update(self):
        self.move()

class Materials(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = random.randint(50, 120)
        height = random.randint(30, 40)
        self.image = pygame.Surface((width, height))
        self.image.fill((35, 31, 32))
        x = random.randint(-10, 450)
        y = random.randint(100, 300)
        self.rect = self.image.get_rect(topleft = (x, y))

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        side = ['right', 'left']
        self.side = random.choice(side)
        self.image = pygame.image.load("heart.png")
        self.image = pygame.transform.rotozoom(self.image, 0, 1.5)
        if self.side == 'right':
            self.rect = self.image.get_rect(topleft = (470, 50))
        else:
            self.rect = self.image.get_rect(topleft = (-10, 50))
    
    def update(self):
        if self.side == 'left':
            self.rect.x += 1
        if self.side == 'right':
            self.rect.x -= 1

class Game:
    def __init__(self):
        self.player = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()
        self.bullet = pygame.sprite.GroupSingle()
        self.mat = pygame.sprite.GroupSingle()
        self.heart = pygame.sprite.GroupSingle()
        self.player.add(Player())
        self.lives = 3
        self.game_active = False
        self.font = pygame.font.Font("Pixeltype.ttf", 40)
        self.cur_time = 0
        self.tot_time = int(pygame.time.get_ticks()/100) - self.cur_time
        self.score = 0
        self.loselife = pygame.mixer.Sound("mixkit-arcade-space-shooter-dead-notification-272.wav")
        self.gameoversound = pygame.mixer.Sound("mixkit-player-losing-or-failing-2042.wav")
        self.obstaclekill = pygame.mixer.Sound("mixkit-arcade-mechanical-bling-210.wav")
        self.gainlife = pygame.mixer.Sound("mixkit-arcade-video-game-bonus-2044.wav")

    def Obstacle_spawn(self):
        self.obstacles.add(Obstacles((random.randint(25,425), random.randint(-100, -50))))

    def check_collision(self):
        if self.bullet:
            if self.obstacles:
                for obstacles in self.obstacles:
                    if pygame.sprite.spritecollide(obstacles, self.bullet, False):
                        obstacles.kill()
                        self.obstaclekill.play()
        
            for player in self.player:
                if Bullet.rebound:
                    pygame.sprite.spritecollide(player, self.bullet, True)

            if self.heart:
                for heart in self.heart:
                    if pygame.sprite.spritecollide(heart, self.bullet, False):
                        heart.kill()
                        self.lives += 1
                        self.gainlife.play()

    def obstacle_crossed(self):
        if self.obstacles:
            for obstacles in self.obstacles:
                if obstacles.rect.top >= 700:
                    self.lives -= 1
                    obstacles.kill()
                    if self.lives>=1:
                        self.loselife.play()

    def bullet_crossed(self):
        if self.bullet:
            for bullet in self.bullet:
                if bullet.rect.top >= 700:
                    self.lives -= 1
                    bullet.kill()
                    if self.lives>=1:
                        self.loselife.play()

    def dis_score(self):
        self.tot_time = int(pygame.time.get_ticks()/100) - self.cur_time
        self.score_surf = self.font.render(f'Score: {game.tot_time}', False, "black")
        self.score_rect = self.score_surf.get_rect(topleft = (180, 10))
        screen.blit(self.score_surf, self.score_rect)
        return self.tot_time

    def dis_lives(self):
        self.lives_surf = self.font.render(f'Lives: {self.lives}', False, 'black')
        self.lives_rect = self.lives_surf.get_rect(topleft = (190, 30))
        screen.blit(self.lives_surf, self.lives_rect)
    
    def check_game_over(self):
        if self.lives == 0:
            self.game_over()
            self.gameoversound.play()
    
    def game_over(self):
        self.game_active = False
        self.bullet.empty()
        self.obstacles.empty()
        self.lives = 3

    def run(self):
        self.player.update()
        self.bullet.update()
        self.obstacles.update()
        self.mat.update()
        self.heart.update()
        self.bullet_crossed()
        self.obstacle_crossed()
        self.check_collision()
        self.check_game_over()
        self.dis_lives()
        self.mat.draw(screen)
        self.obstacles.draw(screen)
        self.player.draw(screen)
        self.bullet.draw(screen)
        self.heart.draw(screen)
        self.score = self.dis_score()

if __name__ == '__main__':
    pygame.init()
    bg_music = pygame.mixer.Sound("music.wav")
    bg_music.set_volume(0.1)
    bg_music.play(loops = -1)
    width = 450
    height = 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Minimal Shooter")
    clock = pygame.time.Clock()
    game = Game()

    OBSTACLESPAWN = pygame.USEREVENT + 1
    pygame.time.set_timer(OBSTACLESPAWN, random.randint(2000,2500))

    OBSTACLESPAWN2 = pygame.USEREVENT + 4
    pygame.time.set_timer(OBSTACLESPAWN2, random.randint(1800, 2000))

    OBSTACLESPAWN3 = pygame.USEREVENT + 5
    pygame.time.set_timer(OBSTACLESPAWN3, random.randint(1500, 1800))

    MATSSPAWN = pygame.USEREVENT + 2
    pygame.time.set_timer(MATSSPAWN, 5500)

    HEARTSPAWN = pygame.USEREVENT + 3
    pygame.time.set_timer(HEARTSPAWN, 11000)

    bulletshot = pygame.mixer.Sound("mixkit-short-laser-gun-shot-1670.wav")        

    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game.game_active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    for player in game.player:
                        if game.bullet:
                            pass
                        else:
                            game.bullet.add(Bullet(player.rect.center, x, y))
                            bulletshot.play()
                        break   
                if game.tot_time < 500:     
                    if event.type == OBSTACLESPAWN:
                        game.Obstacle_spawn()
                elif game.tot_time >= 500 and game.tot_time < 1500:
                    if event.type == OBSTACLESPAWN2:
                        game.Obstacle_spawn()
                else:
                    if event.type == OBSTACLESPAWN3:
                        game.Obstacle_spawn()
                if event.type == MATSSPAWN:
                    game.mat.add(Materials())
                if event.type == HEARTSPAWN:
                    game.heart.add(Heart())
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game.game_active = True
                        game.cur_time = int(pygame.time.get_ticks()/100)
                        
        screen.fill('white')
        if game.game_active:
            game.run()
        else:
            end_surf = game.font.render("Press Space to start!", False, 'black')
            end_rect = end_surf.get_rect(center = (225, 400))
            image_surf = pygame.image.load("green.png")
            image_surf = pygame.transform.rotozoom(image_surf, 0, 5)
            image_rect = image_surf.get_rect(center = (225, 200))
            score_surf = game.font.render(f'Your Score is: {game.score}', False, 'black')
            score_rect = score_surf.get_rect(center = (225, 500))
            font = pygame.font.Font("Pixeltype.ttf", 20)
            font2 = pygame.font.Font("Pixeltype.ttf", 80)
            rule1_surf = font.render("Rules:", True, 'black')
            rule2_surf = font.render("1. Press A to move left and D to move right.", True, 'black')
            rule3_surf = font.render("2. Press mousebutton to shoot towards cursor.", True, 'black')
            rule4_surf = font.render("3. You have only one bullet.", True, 'black')
            rule5_surf = font.render("4. Failure to catch the bullet will result in loss of a life.", True, 'black')
            rule6_surf = font.render("5. Failure to kill an enemy will result in loss of a life.", True, 'black')
            objective_surf = font.render("Objective: Kill as many enemies as possible.", True, 'black')
            title_surf = font2.render("Minimal Shooter", False, 'black')
            title_rect = title_surf.get_rect(center = (225, 50))
            objective_rect = objective_surf.get_rect(topleft = (10, 450))
            rule1_rect = rule1_surf.get_rect(topleft = (10, 500))
            rule2_rect = rule2_surf.get_rect(topleft = (10, 530))
            rule3_rect = rule3_surf.get_rect(topleft = (10, 560))
            rule4_rect = rule4_surf.get_rect(topleft = (10, 590))
            rule5_rect = rule5_surf.get_rect(topleft = (10, 620))
            rule6_rect = rule6_surf.get_rect(topleft = (10, 650))
            if game.score != 0:
                screen.blit(score_surf, score_rect)
            else:
                screen.blit(rule1_surf, rule1_rect)
                screen.blit(rule2_surf, rule2_rect)
                screen.blit(rule3_surf, rule3_rect)
                screen.blit(rule4_surf, rule4_rect)
                screen.blit(rule5_surf, rule5_rect)
                screen.blit(rule6_surf, rule6_rect)
                screen.blit(objective_surf, objective_rect)
            screen.blit(end_surf, end_rect)
            screen.blit(image_surf, image_rect)
            screen.blit(title_surf, title_rect)
        clock.tick(60)
        pygame.display.flip()