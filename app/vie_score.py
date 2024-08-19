import pygame
from pygame import *
from vie import Vie
import random

class Vie_Score(pygame.sprite.Sprite):
    def __init__(self, largeur_ecran):
        super().__init__()
        self.image = pygame.image.load("/home/rigolo/SpaceInvaderII/images/coeur.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(largeur_ecran/2, 10))

        self.compteur_vie = 0
        self.depart = largeur_ecran/2
        self.liste_vie = pygame.sprite.Group()
        

    def gestion_vies_score(self):
        if len(self.liste_vie) < self.compteur_vie:
            vie = Vie_Score(0)
            vie.rect = (self.depart, 10)
            self.liste_vie.add(vie)
            self.depart += 20
        
        if len(self.liste_vie) > self.compteur_vie:
            vie = self.liste_vie.pop()
            vie.kill()
            self.depart -= 20

    #print('v = {} et depart = {}'.format(v, self.depart))

    def draw(self, ecran):
        self.liste_vie.draw(ecran)

    def maj_cpt_vie(self, valeur):
        self.compteur_vie = valeur