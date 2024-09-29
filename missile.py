import pygame
from pygame import *

class Missile(pygame.sprite.Sprite):
    def __init__(self, largeur_ecran, center_missile):
        super().__init__()
        self.image = pygame.image.load("images/missile_blanc.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=center_missile)

        self.largeur_ecran = largeur_ecran
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.largeur_ecran:
            self.kill()