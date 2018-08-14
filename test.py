#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

pygame.init()


def load_pict(file_path, transparent_color=None):
    try:
        pict = pygame.image.load(file_path)

    except pygame.error as message:
        print("picture is missing:", file_path)
        raise SystemExit(message)

    pict = pict.convert()
    if transparent_color is not None:
        if transparent_color is -1:
            transparent_color = pict.get_at((0, 0)) # 左上が透過色になる
        pict.set_colorkey(transparent_color, pygame.RLEACCEL)

    return pict, pict.get_rect()


screen = pygame.display.set_mode((320, 240))

pygame.display.set_caption(u"Window")

jiki = load_pict("./pict/jiki.png", transparent_color=-1)


while True:
    screen.fill((50, 50, 50))  # 画面を青色で塗りつぶす

    pygame.draw.circle(screen, (255, 100, 100), (150, 120), 5)

    screen.blit(jiki, (100, 60))

    pygame.display.update()  # 画面を更新
    # イベント処理

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 終了イベント
            sys.exit()

