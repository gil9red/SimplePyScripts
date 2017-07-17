#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://www.nerdparadise.com/programming/pygame/part1


import pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))

done = False
is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue
            break

    pressed = pygame.key.get_pressed()

    # If Esc clicked
    if pressed[pygame.K_ESCAPE]:
        break

    if pressed[pygame.K_UP]:
        y -= 3

    if pressed[pygame.K_DOWN]:
        y += 3

    if pressed[pygame.K_LEFT]:
        x -= 3

    if pressed[pygame.K_RIGHT]:
        x += 3

    screen.fill((0, 0, 0))

    color = (0, 128, 255) if is_blue else (255, 100, 0)
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))

    pygame.display.flip()

    # will block execution until 1/60 seconds have passed
    # since the previous time clock.tick was called.
    clock.tick(60)
