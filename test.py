#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import math
import random


SCR_RECT = Rect(0, 0, 320, 160)

pygame.display.set_caption(u"Window")

jiki_cur_Position = (0, 0)
jiki_Position = []


START = (300, 40)


def main():

    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)

    tama = pygame.sprite.RenderUpdates()
    Fireball.containers = tama
    Fireball.image = load_image("./pict/fireball.png", colorkey=-1)

    all = pygame.sprite.RenderUpdates()
    player = pygame.sprite.Group()
    pshots = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    eshots = pygame.sprite.Group()

    Player.containers = all, player
    Shot.containers = all, pshots
    EnemyShot.containers = all, eshots
    Alien.containers = all, enemy

    Player.image = load_image("./pict/jiki.png", -1)
    Shot.image = load_image("./pict/Pshot.png")
    EnemyShot.image = load_image("./pict/Eshot.png")
    Alien.images = split_image(load_image("./pict/alien.png", colorkey=-1))

    Player()

    for i in range(0, 11):
        x = 15 + (i % 5) * 20
        y = 15 + (i // 5) * 20

        Alien((x, y))

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        screen.fill((50, 50, 50))

        pygame.draw.circle(screen, (255, 100, 100), (150, 120), 5)

        all.update()
        all.draw(screen)

        collision_detection(player, pshots, enemy, eshots)
        #collision_detection(eshots, player)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()


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


def split_image(image):

    imageList = []

    for i in range(0, 60, 30):
        surface = pygame.Surface((30, 30))
        surface.blit(image, (0, 0), (i, 0, 30, 30))
        surface.set_colorkey(surface.get_at((0, 0)), RLEACCEL)
        surface.convert()
        imageList.append(surface)

    return imageList


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


class EnemyShot(Shot):
    def __init__(self, speed):
        super().__init__(speed)
        self.speed = - 5
        pygame.sprite.Sprite.__init__(self, self.containers)


class Alien(pygame.sprite.Sprite):
    speed = 1
    animcycle = 36
    frame = 0
    move_width = 100
    prob_shots = 0.001

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.left = pos[0]
        self.right = self.left + self.move_width

    def update(self):
        self.rect.move_ip(self.speed, 0)

        if self.rect.center[0] < self.left or self.rect.center[0] > self.right:
            self.speed = -self.speed

        if random.random() < self.prob_shots:
            EnemyShot(self.rect.center)

        self.frame += 1
        self.image = self.images[self.frame // self.animcycle % 2]
        #/のみはPython2の書き方、3は//で整数になる


def collision_detection(player, Pshots, aliens, Eshots):

    alien_collided = pygame.sprite.groupcollide(aliens, Pshots, True, True)

    for alien in alien_collided.keys():
        print(alien)

    player_collided = pygame.sprite.groupcollide(player, Eshots, True, True)
    if player_collided:
        print(player)


if __name__ == "__main__":
    main()
