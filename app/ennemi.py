import pygame
from pygame import *
import random

class Ennemi(pygame.sprite.Sprite):
    def __init__(self, largeur_ecran, hauteur_ecran):
        super().__init__()
        self.image = pygame.image.load("/home/rigolo/SpaceInvaderII/images/ennemi.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.x = largeur_ecran
        self.rect.y = random.randint(0, hauteur_ecran)
        self.speed = 7


    def update(self):
        self.rect.x -= self.speed
        if self.rect.top <= 0:
            self.kill()  # Supprime l'ennemi s'il sort de l'écran