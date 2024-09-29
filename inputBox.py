import pygame
from pygame import *


class InputBox(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, text='Entrer un pseudo'):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.SysFont('/home/rigolo/SpaceInvaderII/police/Neuropol.otf', 40)
        self.color = pygame.Color('white')
        self.txt_surface = self.font.render(text, True, self.color)
        self.entrer = False
        self.text = text
        self.first_key = False
    
    def handle_event_key(self, event):
        if not self.first_key:
            self.text = ""
            self.first_key = True
        self.font = pygame.font.SysFont('/home/rigolo/SpaceInvaderII/police/Neuropol.otf', 40)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.entrer = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        self.txt_surface = self.font.render(self.text, True, self.color)               


    def handle_event_mouse(self, event, recto):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if recto.collidepoint(event.pos):
                self.text = ""
        self.txt_surface = self.font.render(self.text, True, self.color)

    def new_texte(self, new_text):
        self.font = pygame.font.SysFont('/home/rigolo/SpaceInvaderII/police/Neuropol.otf', 30)
        self.text = new_text
        self.txt_surface = self.font.render(self.text, True, self.color)

    def get_text(self):
        return self.text


