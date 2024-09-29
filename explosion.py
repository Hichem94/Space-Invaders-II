import pygame
from pygame import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("images/explosion2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=position)
        
        self.timer = 100
        self.temps_explosion = pygame.time.get_ticks()


    def update(self):
        self.explose()

    def explose(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.temps_explosion >= self.timer:
            self.kill()