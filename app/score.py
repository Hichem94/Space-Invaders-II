import pygame
from pygame import *

class Score(pygame.sprite.Sprite):
    def __init__(self, police, color, taille, largeur_ecran):
        super(Score, self).__init__()
        self.image = pygame.image.load("/home/rigolo/SpaceInvaderII/images/bouclier3.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()
        
        self.position = (largeur_ecran/2, 15)
        self.police = police
        self.color  = color
        self.taille = taille
        self.font   = pygame.font.SysFont(self.police, self.taille)
        self.score_t  = 0


        def update(self):
            affiche_texte(self)
        
        def incremente(self, valeur):
            self.score_t += valeur

        def affiche_texte(self):
            self.image = self.font.render('Score : ' + str(self.score), False, self.color)
            self.rect  = self.image.get_rect(center=self.position)





