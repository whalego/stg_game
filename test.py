#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

pygame.init()

SCR_WIDTH, SCR_HEIGHT = 320,160

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


screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))

pygame.display.set_caption(u"Window")

jikiImg,jikiRect = load_pict("./pict/jiki.png", transparent_color=-1)

jiki_cur_Position = (0, 0)
jiki_Position = []



vx = vy = 1.5
clock = pygame.time.Clock()
jikiRect.left, jikiRect.top = 16, 30# 初期位置
while True:
    clock.tick(60)
    screen.fill((50, 50, 50))  # 画面を青色で塗りつぶす
    pygame.draw.circle(screen, (255, 100, 100), (150, 120), 5)
    jikiRect.move_ip(vx, vy)

    if jikiRect.left < 5 or jikiRect.right > 160:
        vx = -vx
    if jikiRect.top < 5 or jikiRect.bottom > 155:
        vy = -vy

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_LEFT]:
        jikiRect.move_ip(-vx, 0)
    if pressed_keys[K_RIGHT]:
        jikiRect.move_ip(vx, 0)
    if pressed_keys[K_UP]:
        jikiRect.move_ip(-vy, 0)
    if pressed_keys[K_DOWN]:
        jikiRect.move_ip(vy, 0)

    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:
        x, y = pygame.mouse.get_pos()
        x -= jikiImg.get_width() / 2
        y -= jikiImg.get_height() / 2
        jiki_Position.append((x, y))

    x, y = pygame.mouse.get_pos()
    x -= jikiImg.get_width() / 2
    y -= jikiImg.get_height() / 2
    jiki_cur_Position = x, y

    for i, j in jiki_Position:
        screen.blit(jikiImg, (i, j))

    screen.blit(jikiImg, jikiRect)
    pygame.display.update()  # 画面を更新
    # イベント処理

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 終了イベント
            sys.exit()




