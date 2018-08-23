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

        self.load_images()
        self.init_game()

        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def init_game(self):
        self.game_state = START
        self.all = pygame.sprite.RenderUpdates()
        self.player = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.Pshots = pygame.sprite.Group()
        self.Eshots = pygame.sprite.Group()

        Player.containers = self.all, self.player
        Enemy.containers = self.all, self.enemy
        Shot.containers = self.all, self.Pshots
        EShot.containers = self.all, self.Eshots
        Explosion.containers = self.all

        #Player()

        for i in range(0, 11):
            x = 15 + (i % 5) * 20
            y = 15 + (i // 5) * 20
            Enemy((x, y))

    def update(self):
        if self.game_state == PLAY:
            self.all.update()
            self.collision_detection()

            if len(self.enemy.sprites()) == 0:
                self.game_state = GAMEOVER

    def draw(self, screen):
        screen.fill((50, 50, 50))

        if self.game_state == START:
            title_font = pygame.font.SysFont(None, 80)#Fontの使い方調べる
            title = title_font.render("START GAME", False, (255, 0, 0))
            screen.blit(title, ((SCR_RECT.width - title.get_width()) // 2, 50))

            enemy_image = Enemy.images[0]
            screen.blit(enemy_image, ((SCR_RECT.width-enemy_image.get_width()) // 2, 100))

            push_font = pygame.font.SysFont(None, 80)
            push_space = push_font.reder("PUSH SPACE KEY", False, (255, 125, 125))
            screen.blit = (push_space, ((SCR_RECT.width - push_space.get_width()) // 2, 150))

            credit_font = pygame.font.SysFont(None, 80)
            credit_space = credit_font.reder("くれじっと", False, (255, 125, 125))
            screen.blit = (credit_space, ((SCR_RECT.width - credit_space.get_width()) // 2, 150))

        elif self.game_state == PLAY:
            self.all.draw(screen)

        elif self.game_state == GAMEOVER:
            gameover_font = pygame.font.SysFont(None, 80)
            gameover = gameover_font.render("GAME OVER", False, (255,0,0))
            screen.blit(gameover, ((SCR_RECT.width - gameover.get_width()) // 2, 50))
            # エイリアンを描画
            enemy_image = Enemy.images[0]
            screen.blit(enemy_image, ((SCR_RECT.width - enemy_image.get_width()) // 2, 100))
            # PUSH STARTを描画
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", False, (255,255,255))
            screen.blit(push_space, ((SCR_RECT.width - push_space.get_width()) // 2, 150))

    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and event.key == K_SPACE:
                if self.game_state == START:
                    self.game_state = PLAY

                elif self.game_state == GAMEOVER:
                    self.init_game()
                    self.game_state = PLAY

    def collision_detection(self):
        enemy_collided = pygame.sprite.groupcollide(self.enemy, self.shots, True, True)
        for enemy in enemy_collided.keys():
            Explosion(enemy.rect.center)

        player_collided = pygame.sprite.groupcollide(self.player, self.Eshots, True, True)
        if player_collided:
            print(self.player)

        Eshots_collided = pygame.sprite.groupcollide(self.Eshots, self.Pshots, True, True)
        for exp in Eshots_collided.keys():
            Explosion(exp.rect.center)

    def load_images(self):
        Player.image = load_image("./pict/jiki.png", -1)
        Shot.image = load_image("./pict/Pshot.png")
        EShot.image = load_image("./pict/Eshot.png")
        Enemy.images = split_image(load_image("./pict/enemy.png", -1), 2)
        Explosion.images = split_image(load_image("./pict/bomb.png", -1), 5)

    def load_sounds(self):
        pass


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


class EShot(Shot):
    def __init__(self, speed):
        super().__init__(speed)
        self.speed = - 3
        #pygame.sprite.Sprite.__init__(self, self.containers)


class Enemy(pygame.sprite.Sprite):
    speed = 1
    animcycle = 36
    frame = 0
    move_width = 100
    prob_shots = 0.004

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
            EShot(self.rect.center)

        self.frame += 1
        self.image = self.images[self.frame // self.animcycle % 2]
        #/のみはPython2の書き方、3は//で整数になる


def split_image(image, n):

    imageList = []
    w = image.get_width()
    h = image.get_height()
    wl = w / n

    for i in range(0, w, h):
        surface = pygame.Surface((wl, h))
        surface.blit(image, (0, 0), (i, 0, wl, h))
        surface.set_colorkey(surface.get_at((0, 0)), RLEACCEL)
        surface.convert()
        imageList.append(surface)

    return imageList


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


class Explosion(pygame.sprite.Sprite):

    animcycle = 2
    frame = 0

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.max_frame = len(self.images) * self.animcycle

    def update(self):
        self.image = self.images[self.frame // self.animcycle]
        self.frame += 1
        if self.frame == self.max_frame:
            self.kill()


if __name__ == "__maine__":
    Invader()
