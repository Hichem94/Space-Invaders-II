import pygame
from pygame import *
from missile import Missile


class Vaisseau(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/home/rigolo/SpaceInvaderII/images/vaisseau.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()

        self.speed = 15
        self.missiles = pygame.sprite.Group()

        self.missile_ready = True
        self.temps_reload_missile = 100
        self.temps_depart_missile = 0


        self.bouclier_image = pygame.image.load("/home/rigolo/SpaceInvaderII/images/bubble.png").convert_alpha()
        self.bouclier_image = pygame.transform.scale(self.bouclier_image, (80, 70))
        self.bouclier_image.set_colorkey((255, 255, 255), RLEACCEL)
        self.bouclier_rect = self.bouclier_image.get_rect()
        self.bouclier_active = False
        self.bouclier_duree = 6000
        self.bouclier_consume = 0
        

    def handle_mouvement(self, keys, largeur_ecran, hauteur_ecran):
        if keys[K_UP]:
            self.rect.y -= 15
        if keys[K_DOWN]:
            self.rect.y += 15
        if keys[K_RIGHT]:
            self.rect.x += 15
        if keys[K_LEFT]:
            self.rect.x -= 15
        
        # Le vaisseau reste dans l'écran
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largeur_ecran:
            self.rect.right = largeur_ecran
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= hauteur_ecran:
            self.rect.bottom = hauteur_ecran


    def update(self):
        self.missiles.update()
        self.reload_missile()
        self.check_armor()

    def shoot_missile(self, largeur_ecran):
        if self.missile_ready:
            missile = Missile(largeur_ecran, self.rect.center)
            self.missiles.add(missile)
            self.temps_depart_missile = pygame.time.get_ticks()
            self.missile_ready = False

    def reload_missile(self):
        if self.missile_ready == False:
            current_time = pygame.time.get_ticks()
            if current_time - self.temps_depart_missile >= self.temps_reload_missile:
                self.missile_ready = True


    def armor(self):
        if not self.bouclier_active:
            self.bouclier_active = True
            self.bouclier_consume = pygame.time.get_ticks()
        else:
            self.bouclier_consume += self.bouclier_duree
    
    def check_armor(self):
        if self.bouclier_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.bouclier_consume >= self.bouclier_duree:
                self.bouclier_active = False


    def draw(self, ecran):
        # Dessiner les missiles
        #ecran.blit(self.image, self.rect)
        self.missiles.draw(ecran)
        # Dessiner le bouclier autour du vaisseau s'il est actif
        if self.bouclier_active:
            self.bouclier_rect.center = self.rect.center
            ecran.blit(self.bouclier_image, self.bouclier_rect)

        
            