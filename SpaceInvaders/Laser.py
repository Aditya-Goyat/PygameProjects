import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, height, speed = 8):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill("white")
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height = height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height + 50:
            self.kill()

    def update(self):
        self.rect.y -= self.speed
        self.destroy()