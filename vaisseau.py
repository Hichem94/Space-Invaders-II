import pygame
from pygame import *
from missile import Missile
from vie import Vie

class Vaisseau(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/vaisseau.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()

        # Missile
        self.speed = 15
        self.missiles = pygame.sprite.Group()
        self.missile_ready = True
        self.temps_reload_missile = 100
        self.temps_depart_missile = 0

        # Bouclier
        self.bouclier_active = False
        self.bouclier_duree = 6000
        self.bouclier_consume = 0

        # Vie
        self.vies = 1
        #self.vie  = Vie(0,0,0)

        # Vie score
        self.depart = 1000/2
        self.liste_vie = []
        self.groupe_vie = pygame.sprite.Group()
        

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
        zone_interdite = 15
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largeur_ecran:
            self.rect.right = largeur_ecran
        if self.rect.top <= zone_interdite:
            self.rect.top = zone_interdite
        if self.rect.bottom >= hauteur_ecran:
            self.rect.bottom = hauteur_ecran-zone_interdite


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


    def add_vie(self):
        self.vies += 1

    def remove_vie(self):
        self.vies -= 1
    
    def get_vies(self):
        return self.vies

    def gestion_vies_score(self):
        #print('len(liste_vie) = {} et self.vies = {}'.format(len(self.liste_vie), self.vies))
        if len(self.liste_vie) < self.vies:
            vie = Vie(0,0,0)
            vie.image = pygame.transform.scale(vie.image, (20, 20))
            vie.rect = (self.depart, 10)
            self.liste_vie.append(vie)
            self.groupe_vie.add(vie)
            self.depart += 20
        
        if len(self.liste_vie) > self.vies:
            vie = self.liste_vie[len(self.liste_vie)-1]
            self.liste_vie.pop()
            self.groupe_vie.remove(vie)
            vie.kill()
            self.depart -= 20

    def draw(self, ecran):
        # Dessiner les missiles
        #ecran.blit(self.image, self.rect)
        self.missiles.draw(ecran)
        self.groupe_vie.draw(ecran)
        # Dessiner le bouclier autour du vaisseau s'il est actif
        if self.bouclier_active:
            bouclier_image = pygame.image.load("/images/bubble.png").convert_alpha()
            bouclier_image = pygame.transform.scale(bouclier_image, (80, 70))
            bouclier_image.set_colorkey((255, 255, 255), RLEACCEL)
            bouclier_rect = bouclier_image.get_rect()
            bouclier_rect.center = self.rect.center
            ecran.blit(bouclier_image, bouclier_rect)
            

    def kill_missile(self):
        for missile in self.missiles:
            missile.kill()
            