import pygame
import sys
from pygame import *
from inputBox import InputBox
from background import Background
import database as db

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

    


def menu(ecran, running_game_over, score, menu_sound):

    player_pseudo = ""

    largeur_ecran, hauteur_ecran = pygame.display.get_surface().get_size()
    bgd_a = Background("/home/rigolo/SpaceInvaderII/images/invaders.png", largeur_ecran, hauteur_ecran, 0, 0)
    background_group_a = pygame.sprite.GroupSingle(bgd_a)
    # bgd_b = Background("/home/rigolo/SpaceInvaderII/images/feuille.png", 600, 500, 300, 300)
    # background_group_b = pygame.sprite.GroupSingle(bgd_b)

    if running_game_over:
        running_menu  = False
    else:
        running_menu = True
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
    
    while True:

        # Menu principal
        while running_menu:
            
            #ecran.fill("#222023") # Couleur de fond
            background_group_a.draw(ecran)

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
                    running_menu  = False
                    running_input = False
                    running_score = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:   # JOUER
                        menu_sound.play()
                        running_menu = False
                        running_input = True
                        break
                    if event.key == pygame.K_2:   # SCORE
                        menu_sound.play()
                        running_menu = False
                        running_score = True
                        break
                    if event.key == pygame.K_3:   # QUITTER
                        menu_sound.play()
                        running_menu = False
                        pygame.quit()
                        sys.exit()                

            pygame.display.flip()



        # Entrer le pseudo    
        pygame.display.flip()
        inputbox = InputBox(380,380,100,100)
        recto = pygame.Rect(250, 350, 500, 100) # Rectangle autour de la zone de texte
        while running_input:
            #ecran.fill("#222023") # Couleur de fond
            background_group_a.draw(ecran)
            
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


        # Scores
        while running_score:
            #ecran.fill("#222023") # Couleur de fond
            background_group_a.draw(ecran)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_menu  = False
                    running_input = False
                    running_score = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        menu_sound.play()
                        running_score = False
                        running_menu  = True

            # Afficher HIGH SCORES
            gestion_texte(ecran, "H", YELLOW, '/home/rigolo/SpaceInvaderII/police/Game_Of_Squids.otf', 80, (270, 200))
            gestion_texte(ecran, "I", RED, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 80, (320, 200))
            gestion_texte(ecran, "GH", YELLOW, '/home/rigolo/SpaceInvaderII/police/Game_Of_Squids.otf', 80, (350, 200))
            gestion_texte(ecran, " SC", YELLOW, '/home/rigolo/SpaceInvaderII/police/Game_Of_Squids.otf', 80, (450, 200))
            gestion_texte(ecran, "O", RED, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 80, (623, 200))
            gestion_texte(ecran, "R", YELLOW, '/home/rigolo/SpaceInvaderII/police/Game_Of_Squids.otf', 80, (655, 200))
            gestion_texte(ecran, "E", RED, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 80, (705, 200))
            gestion_texte(ecran, "S", YELLOW, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 80, (730, 200))
            
            # Afficher 1. 2. 3. 4. 5.
            gestion_texte(ecran, "1. ", YELLOW, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 60, (390, 350))
            gestion_texte(ecran, "2. ", YELLOW, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 60, (390, 390))
            gestion_texte(ecran, "3. ", YELLOW, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 60, (390, 430))
            gestion_texte(ecran, "4. ", YELLOW, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 60, (390, 470))
            gestion_texte(ecran, "5. ", YELLOW, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 60, (390, 510))
            
            # Afficher player et score
            scores = db.best_scores()
            #print(scores)
            y = 350
            for t in scores:
                pseudo = t[0]
                score  = t[1]
                s      = pseudo + " (" + str(score) + ")"
                gestion_texte(ecran, s, WHITE, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 60, (440, y))
                y += 40

            # Afficher "Appuyer sur espace pour quitter."
            gestion_texte(ecran, "Appuyer sur espace pour quitter.", WHITE, '/home/rigolo/SpaceInvaderII/police/Neuropol.otf', 16, (340, 700))

            pygame.display.flip()
        

        # Game over
        while running_game_over:
            background_group_a.draw(ecran)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_menu      = False
                    running_input     = False
                    running_score     = False
                    running_game_over = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        menu_sound.play()
                        running_game_over = False
                        running_menu      = True

            # Afficher GAME OVER
            s = "SCORE : " + str(score)
            gestion_texte(ecran, "GAME OVER", RED, '/home/rigolo/SpaceInvaderII/police/Game_Of_Squids.otf', 80, (270, 200))
            gestion_texte(ecran, s, YELLOW, '/home/rigolo/SpaceInvaderII/police/Thelamonblack.ttf', 60, (390, 350))

            # Afficher "Appuyer sur espace pour quitter."
            gestion_texte(ecran, "Appuyer sur espace pour quitter.", WHITE, '/home/rigolo/SpaceInvaderII/police/Neuropol.otf', 16, (340, 550))

            pygame.display.flip()

        if not running_menu and not running_input and not running_score and not running_game_over:
            break
    
    return player_pseudo
