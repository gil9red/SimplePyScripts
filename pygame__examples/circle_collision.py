#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import random

import pygame


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)


class Ball(pygame.sprite.Sprite):
    def __init__(self, size, pos=(0, 0), color=WHITE):
        super().__init__()

        self.image = pygame.Surface([size, size], pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, [0, 0, size, size])

        # Для правильной работы функции pygame.sprite.Group.draw
        self.rect = self.image.get_rect()
        self.rect.center = pos

        # Для правильной работы функции pygame.sprite.collide_circle
        self.radius = size // 2


pygame.init()

color = BLACK
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
x, y = random.randrange(0, 500), random.randrange(0, 500)

fnt = pygame.font.Font(None, 40)

ball_1 = Ball(size=100, pos=(x, y), color=BLACK)
ball_2 = Ball(size=50, color=BLACK)

balls = pygame.sprite.Group()
balls.add(ball_1)
balls.add(ball_2)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            ball_2.rect.center = event.pos
            break

    screen.fill(WHITE)
    balls.draw(screen)

    if pygame.sprite.collide_circle(ball_1, ball_2):
        color = BLACK
    else:
        color = WHITE

    text = fnt.render("Collision!", True, color)
    screen.blit(text, (260, 20))

    pygame.display.update()
    clock.tick(60)
