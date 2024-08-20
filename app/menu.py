import pygame
import sys
from pygame import *
from inputBox import InputBox

# Définir les couleurs
WHITE  = (255, 255, 255)
YELLOW = (255, 255, 0)
RED    = (255, 0, 0)

# Gestion de la police
def gestion_texte(ecran, texte, couleur, police, taille, position):
    font = pygame.font.Font(police, taille)
    texte = font.render(texte, True, couleur)
    ecran.blit(texte, position)


def afficher_titre(ecran):

    gestion_texte(ecran, "SP", YELLOW, '/home/rigolo/SpaceInvaderII/police/Game_Of_Squids.otf', 80, (150, 200))
    gestion_texte(ecran, "A", RED, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 80, (270, 200))
    gestion_texte(ecran, "C", YELLOW, '/home/rigolo/SpaceInvaderII/police/Game_Of_Squids.otf', 80, (305, 200))
    gestion_texte(ecran, "E", RED, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 80, (355, 200))
    gestion_texte(ecran, " INV", YELLOW, '/home/rigolo/SpaceInvaderII/police/Game_Of_Squids.otf', 80, (400, 200))
    gestion_texte(ecran, "A", RED, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 80, (547, 200))
    gestion_texte(ecran, "D", YELLOW, '/home/rigolo/SpaceInvaderII/police/Game_Of_Squids.otf', 80, (580, 200))
    gestion_texte(ecran, "E", RED, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 80, (630, 200))
    gestion_texte(ecran, "RS", YELLOW, '/home/rigolo/SpaceInvaderII/police/Game_Of_Squids.otf', 80, (660, 200))
    gestion_texte(ecran, "II", RED, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 80, (780, 200))

    gestion_texte(ecran, "They are back !", WHITE, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 50, (600, 270))

    


def menu(ecran):

    player_pseudo = ""

    running_menu  = True
    running_input = False
    running_score = False 

    # Image du vaisseau
    vaisseau_image = pygame.image.load("/home/rigolo/SpaceInvaderII/images/vaisseau.png").convert_alpha()
    vaisseau_image = pygame.transform.scale(vaisseau_image, (300, 300))
    vaisseau_image.set_colorkey((255, 255, 255), RLEACCEL)
    vaisseau_rect = vaisseau_image.get_rect(center=(200, 420))

    # Image ennemi
    ennemi_image = pygame.image.load("/home/rigolo/SpaceInvaderII/images/ennemi.png").convert_alpha()
    ennemi_image = pygame.transform.scale(ennemi_image, (200, 200))
    ennemi_image.set_colorkey((255, 255, 255), RLEACCEL)
    ennemi_rect = ennemi_image.get_rect(center=(760, 420))
    
    # Menu principal
    while running_menu:
        
        ecran.fill("#222023") # Couleur de fond

        ecran.blit(vaisseau_image, vaisseau_rect)
        ecran.blit(ennemi_image, ennemi_rect)
        
        afficher_titre(ecran)

        gestion_texte(ecran, "JOUER       1", WHITE, '/home/rigolo/SpaceInvaderII/police/Deep_Shadow.ttf', 30, (350, 350))
        gestion_texte(ecran, "SCORES    2", WHITE, '/home/rigolo/SpaceInvaderII/police/Deep_Shadow.ttf', 30, (350, 400))
        gestion_texte(ecran, "QUITTER 3", WHITE, '/home/rigolo/SpaceInvaderII/police/Deep_Shadow.ttf', 30, (350, 450))

        instructions  = "Utiliser les fleches directionnelles de votre clavier pour piloter votre vaisseau spatial."
        gestion_texte(ecran, instructions, WHITE, '/home/rigolo/SpaceInvaderII/police/Neuropol.otf', 16, (60, 600))
        instructions = "Appuyer sur la touche espace pour tirer sur vos ennemis. A vous de jouer !"
        gestion_texte(ecran, instructions, WHITE, '/home/rigolo/SpaceInvaderII/police/Neuropol.otf', 16, (90, 620))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:   # JOUER
                    running_menu = False
                    running_input = True
                    break
                if event.key == pygame.K_2:   # SCORE
                    running_menu = False
                    running_score = True
                    break
                if event.key == pygame.K_3:   # QUITTER
                    running_menu = False
                    pygame.quit()
                    sys.exit()                

        pygame.display.flip()



    # Entrer le pseudo    
    pygame.display.flip()
    inputbox = InputBox(380,380,100,100)
    recto = pygame.Rect(250, 350, 500, 100) # Rectangle autour de la zone de texte
    while running_input:
        ecran.fill("#222023") # Couleur de fond
        afficher_titre(ecran)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                inputbox.handle_event_key(event)
                if inputbox.entrer:
                    if inputbox.text != "":
                        player_pseudo = inputbox.get_text()
                        running_input = False
                        break
                    else:
                        new_texte = "Le pseudo ne peut être vide"
                        inputbox.new_texte(new_texte)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                inputbox.handle_event_mouse(event, recto)

            # Dessiner le rectangle
            pygame.draw.rect(ecran, (255,255,255), recto,  2)
            # Input
            ecran.blit(inputbox.txt_surface, inputbox.rect)
            pygame.display.flip()

    return player_pseudo
