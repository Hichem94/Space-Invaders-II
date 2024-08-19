import pygame
from vaisseau import Vaisseau
from ennemi import Ennemi
from background import Background
from bouclier import Bouclier
import random

# Initialisation de Pygame
pygame.init()


clock = pygame.time.Clock()

# Dimensions de la fenêtre
largeur_ecran, hauteur_ecran = 800, 600
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Space Invaders II")


# Background
background_group = pygame.sprite.Group()
background_ready = True
temps_nouveau_background = 300
temps_depart_background = 0

# Vaisseau
vaisseau = Vaisseau()
tous_les_sprites = pygame.sprite.Group(vaisseau)

# Ennemis
ennemi_group = pygame.sprite.Group()
temps_nouvel_ennemi = 600
temps_depart_ennemi = pygame.time.get_ticks()

# Bouclier
bouclier_group = pygame.sprite.Group()
temps_nouveau_bouclier = random.randint(1000, 3000)
temps_depart_bouclier = pygame.time.get_ticks()

running = True
while running:
    clock.tick(30)  # Limite le FPS à 60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Blit le texte à sa position
    ecran.blit(text, text_rect)

    # Gestion du background
    current_time = pygame.time.get_ticks()
    if current_time - temps_depart_background > temps_nouveau_background:
        bground = Background(largeur_ecran, hauteur_ecran)
        background_group.add(bground)
        tous_les_sprites.add(bground)
        temps_depart_background = current_time   
    
    keys = pygame.key.get_pressed()

    # Gère les entrées clavier pour le vaisseau
    vaisseau.handle_mouvement(keys, largeur_ecran, hauteur_ecran)

    # Tirer un missile avec la touche Espace    
    if keys[pygame.K_SPACE]:        
        vaisseau.shoot_missile(largeur_ecran)

    # Génère un ennemi toutes les 0.6 secondes
    current_time = pygame.time.get_ticks()
    if current_time - temps_depart_ennemi > temps_nouvel_ennemi:
        ennemi = Ennemi(largeur_ecran, hauteur_ecran)
        ennemi_group.add(ennemi)
        tous_les_sprites.add(ennemi)
        temps_depart_ennemi = current_time

    # Génère un bouclier aléatoirement entre 1 et 10 secondes 
    current_time = pygame.time.get_ticks()
    if current_time - temps_depart_bouclier > temps_nouveau_bouclier:
        bouclier = Bouclier(largeur_ecran, hauteur_ecran)
        bouclier_group.add(bouclier)
        tous_les_sprites.add(bouclier)
        temps_depart_bouclier = current_time

    # Collision Missile / Ennemi
    for missile in vaisseau.missiles:
        ennemis_touches = pygame.sprite.spritecollide(missile, ennemi_group, True)
        if ennemis_touches:
            missile.kill()

    # Collision Vaisseau / Ennemi
    if pygame.sprite.spritecollide(vaisseau, ennemi_group, False) and not vaisseau.bouclier_active:
        running = False  # Termine le jeu si le vaisseau touche un ennemi

    # Collision Vaisseau+Bouclier / Ennemi
    if pygame.sprite.spritecollide(vaisseau, ennemi_group, True) and vaisseau.bouclier_active:
        pass

    # Collision Vaisseau / Bouclier
    if pygame.sprite.spritecollide(vaisseau, bouclier_group, True):
        vaisseau.armor()

    # Met à jour tous les sprites
    tous_les_sprites.update()

    # Affichage
    ecran.fill("#222023")
    tous_les_sprites.draw(ecran)
    vaisseau.draw(ecran)
    pygame.display.update()

    # Mettre à jour l'écran
    pygame.display.flip()

pygame.quit()