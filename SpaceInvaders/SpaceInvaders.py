import pygame, sys
from Player import Player
import Obstacles
from Alien import Alien
from random import choice, randint
from Laser import Laser
from Alien import Extra

class Game:
    def __init__(self):
        #Player setup
        player_sprite = Player((300,600), width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #obstacle setup
        self.shape = Obstacles.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (width/self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles( self.obstacle_x_positions, x_start = width/15 , y_start = 450,)

        #alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1

        #laser setup
        self.alien_lasers = pygame.sprite.Group()

        #extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,800)
    
    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Obstacles.Block(self.block_size, (241,79,80), x, y)
                    self.blocks.add(block)
    
    def create_multiple_obstacles(self, offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_pos_check(self):
        for alien in self.aliens:
            if alien.rect.right >= width:
                self.alien_direction = -1
                self.alien_move_down(2)
            if alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens:
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens:
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, height, -6)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_spawn(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), width))
            self.extra_spawn_time = randint(600,800)

    def collision_checks(self):
        #player lasers
        if self.player.sprite.laser:
            for laser in self.player.sprite.laser:
                #obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                #alien collisions
                if pygame.sprite.spritecollide(laser, self.aliens, True):
                    laser.kill()

                #extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                        laser.kill()

        #alien laser
        if self.alien_lasers:
            for laser in self.alien_lasers:
                #obstacle collision
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                
                #player collision
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
            
        #aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()
        

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_pos_check()
        self.alien_lasers.update()
        self.extra_alien_spawn()
        self.extra.update()
        self.collision_checks()
        self.player.draw(screen)
        self.player.sprite.laser.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)

if __name__ == '__main__':
    pygame.init()
    width = 600
    height = 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30,30,30))
        game.run()
        clock.tick(60)
        pygame.display.flip()