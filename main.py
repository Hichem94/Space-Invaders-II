import pygame
from vaisseau import Vaisseau
from ennemi import Ennemi
from background import Background
from bouclier import Bouclier
from explosion import Explosion
from vie import Vie
from menu import menu
import database as db
import random

# Initialisation de Pygame
pygame.init()

# Sounds
pygame.mixer.init()
shoot_sound     = pygame.mixer.Sound("/home/rigolo/SpaceInvaderII/sounds/shoot.wav")
explosion_sound = pygame.mixer.Sound("/home/rigolo/SpaceInvaderII/sounds/explosion.wav")
explosion_sound.set_volume(0.3)
bonus_sound     = pygame.mixer.Sound("/home/rigolo/SpaceInvaderII/sounds/bonus.wav")
menu_sound      = pygame.mixer.Sound("/home/rigolo/SpaceInvaderII/sounds/menu.mp3")
game_over_sound = pygame.mixer.Sound("/home/rigolo/SpaceInvaderII/sounds/game_over.wav")
music           = pygame.mixer.Sound("/home/rigolo/SpaceInvaderII/sounds/music.mpeg")

# Dimensions de la fenêtre
largeur_ecran, hauteur_ecran = 1000, 800
zone_interdite = 50
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Space Invaders II")

#Pour acceder à la page game over
running_game_over = False

# Initialiser le module de police
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 36)
score = 0


# Définir les couleurs
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

while True:

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
    temps_nouveau_bouclier = random.randint(10000, 20000)
    temps_depart_bouclier = pygame.time.get_ticks()

    # Vie
    vie_group = pygame.sprite.Group()
    temps_nouvelle_vie = random.randint(10000, 20000)
    temps_depart_vie = pygame.time.get_ticks()


    music.play(-1)
    player_pseudo = menu(ecran, running_game_over, score, menu_sound)
    score = 0
    running_game_over = False
    
    # Boucle principale
    running = True
    while running:
        clock.tick(30)  # Limite le FPS à 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Maj du score des vies
        # print(vie_score.compteur_vie)
        # vie_score.maj_cpt_vie(vaisseau.get_vies())
        vaisseau.gestion_vies_score()

        # Gestion du background
        current_time = pygame.time.get_ticks()
        if current_time - temps_depart_background > temps_nouveau_background:
            bground = Background("/home/rigolo/SpaceInvaderII/images/background_star_yellow.png", 30, 30, largeur_ecran, hauteur_ecran)
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
            ennemi = Ennemi(zone_interdite, largeur_ecran, hauteur_ecran-zone_interdite)
            ennemi_group.add(ennemi)
            tous_les_sprites.add(ennemi)
            temps_depart_ennemi = current_time

        # Génère un bouclier aléatoirement entre 1 et 10 secondes 
        current_time = pygame.time.get_ticks()
        if current_time - temps_depart_bouclier > temps_nouveau_bouclier:
            bouclier = Bouclier(zone_interdite, largeur_ecran, hauteur_ecran)
            bouclier_group.add(bouclier)
            tous_les_sprites.add(bouclier)
            temps_depart_bouclier = current_time
        
        # Génère une vie aléatoirement entre 1 et 10 secondes
        current_time = pygame.time.get_ticks()
        if current_time - temps_depart_vie > temps_nouvelle_vie:
            vie = Vie(zone_interdite, largeur_ecran, hauteur_ecran)
            vie_group.add(vie)
            tous_les_sprites.add(vie)
            temps_depart_vie = current_time

        # Collision Missile / Ennemi
        for missile in vaisseau.missiles:
            ennemis_touches = pygame.sprite.spritecollide(missile, ennemi_group, True)
            if ennemis_touches:
                explosion = Explosion(missile.rect.center)
                tous_les_sprites.add(explosion)
                explosion_sound.play()
                score += len(ennemis_touches)
                missile.kill()

        # Collision Vaisseau / Ennemi
        ennemis_touches = pygame.sprite.spritecollide(vaisseau, ennemi_group, False)
        for ennemi in ennemis_touches:
            explosion1 = Explosion(ennemi.rect.center)
            tous_les_sprites.add(explosion1)
            score += len(ennemis_touches)
            ennemi.kill()
            if not vaisseau.bouclier_active:
                vaisseau.remove_vie()
            if not vaisseau.get_vies():
                explosion2 = Explosion(vaisseau.rect.center)
                tous_les_sprites.add(explosion2)
                game_over_sound.play()
                
                running = False         # Termine la partie
                running_game_over = True # Pour l'affichage de la page game over
                
                # Ménage
                vaisseau.kill_missile()
                for sprite in tous_les_sprites:
                    sprite.kill()
                #score = 0
                pygame.time.delay(2000)
                break


        # Collision Vaisseau+Bouclier / Ennemi
        if pygame.sprite.spritecollide(vaisseau, ennemi_group, True) and vaisseau.bouclier_active:
            explosion_sound.play()

        # Collision Vaisseau / Bouclier
        if pygame.sprite.spritecollide(vaisseau, bouclier_group, True):
            bonus_sound.play()
            vaisseau.armor()
        
        # Collision Vaisseau / Vie
        if pygame.sprite.spritecollide(vaisseau, vie_group, True):
            bonus_sound.play()
            vaisseau.add_vie()

        # Met à jour tous les sprites
        tous_les_sprites.update()

        # Affichage
        ecran.fill("#222023") # Couleur de fond
        tous_les_sprites.draw(ecran)
        vaisseau.draw(ecran)    

        # Créer le texte du score
        score_text = font.render(f"Score: {score}", True, WHITE)

        # Blit le texte du score en haut à gauche
        ecran.blit(score_text, (largeur_ecran-150, 10))

        pygame.display.update()

    if player_pseudo and score:
        db.ajouter_player_et_score(player_pseudo, score)