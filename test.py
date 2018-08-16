#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import math
import time

#SCR_WIDTH, SCR_HEIGHT = 320, 160
#screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))

SCR_RECT = Rect(0, 0, 320, 160)

pygame.display.set_caption(u"Window")

#jikiImg, jikiRect = load_pict("./pict/jiki.png", transparent_color=-1)

jiki_cur_Position = (0, 0)
jiki_Position = []

"""vx = vy = 1.5"""


START = (300, 40)


def main():

    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)

    tama = pygame.sprite.RenderUpdates()
    Fireball.containers = tama
    Fireball.image = load_image("./pict/fireball.png", colorkey=-1)

    jiki = pygame.sprite.RenderUpdates()
    Player.containers = jiki
    Player.image = load_image("./pict/jiki.png", -1)
    Shot.image = load_image("./pict/shot.png")
    Shot.containers = jiki
    clock = pygame.time.Clock()

    Player()

    while True:
        clock.tick(60)
        screen.fill((50, 50, 50))

        pygame.draw.circle(screen, (255, 100, 100), (150, 120), 5)

        """自機の移動
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
            jikiRect.move_ip(0, -vy)
        if pressed_keys[K_DOWN]:
            jikiRect.move_ip(0, vy)

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
        """

        #mouse_handler()

        tama.update()
        tama.draw(screen)

        jiki.update()
        jiki.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

"""

def mouse_handler():
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:
        x, y = pygame.mouse.get_pos()
        Fireball(START, (x, y))
"""

def load_image(filename, colorkey=None):
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("cant load image:", filename)
        raise SystemExit(message)

    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


class Fireball(pygame.sprite.Sprite):
    speed = 10

    def __init__(self, start, target):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.start = start
        self.target = target
        self.rect.center = self.start

        self.direction = math.atan2(target[1] - start[1], target[0] - start[0])

        self.vx = math.cos(self.direction) * self.speed
        self.vy = math.sin(self.direction) * self.speed

    def update(self):
        self.rect.move_ip(self.vx, self.vy)

        if not SCR_RECT.contains(self.rect):
            self.kill()


class Player(pygame.sprite.Sprite):
    speed = 5
    reload_time = 20

    def __init__(self):
        #imageとcontainersはメインでセットする。
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.bottom
        self.reload_timer = 0

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        pressed_mouse_key = pygame.mouse.get_pressed()

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        self.rect.clamp_ip(SCR_RECT)

        if pressed_mouse_key[0]:
            if self.reload_timer > 0:
                self.reload_timer -= 1
            else:
                Shot(self.rect.center)
                self.reload_timer = self.reload_time


class Shot(pygame.sprite.Sprite):
        speed = 9

        def __init__(self, pos):
            pygame.sprite.Sprite.__init__(self, self.containers)
            self.rect = self.image.get_rect()
            self.rect.center = pos

        def update(self):
            self.rect.move_ip(0, - self.speed)
            if self.rect.top < 0:
                self.kill()


class Alien(pygame.sprite.Sprite):
    speed = 2
    animcycle = 18
    frame = 0
    move_width = 230

    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.left = pos[0]
        self.right = self.left + self.move_width
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.center[0] < self.left or self.rect.center[0] > self.right:
            self.speed = - self.speed
        self.frame+= 1
        self.image = self.images[self.frame/self.animcycle % 2]


if __name__ == "__main__":
    main()
