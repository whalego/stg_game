#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import random

START, PLAY, GAMEOVER = (0, 1, 2)
SCR_RECT = Rect(0, 0, 320, 240)


class Invader:

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("STG画面")

    while True:
        self.update()
        self.draw(screen)
        pygame.display.update()
        self.key_hundler()

    def init_game(self):
        self.game_state = START
        self.all = pygame.sprite.RenderUpdates()
        self.player = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.Pshots = pygame.sprite.Group()
        self.Eshots = pygame.sprite.Group()




if __name__ == "__main__":
    Invader()

