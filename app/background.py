import pygame
from pygame import *
import random

class Background(pygame.sprite.Sprite):

    def __init__(self, largeur_ecran, hauteur_ecran):
        super().__init__()
        self.image = pygame.image.load("/home/rigolo/SpaceInvaderII/images/background_star_yellow.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.x = largeur_ecran
        self.rect.y = random.randint(0, hauteur_ecran)
        self.speed = 5
    
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x <= 0:
            self.kill()