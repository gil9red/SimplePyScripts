#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pygame
import pygame


FPS = 60
W = 700  # ширина экрана
H = 300  # высота экрана
WHITE = (255, 255, 255)
BLUE = (0, 70, 225)

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# координаты и радиус круга
x = W // 2
y = H // 2
r = 50

step = 4

game_active = True

while True:
    # Получение всех событий
    for event in pygame.event.get():
        # Проверка события "Выход"
        if event.type == pygame.QUIT:
            game_active = False
            break

    if not game_active:
        break

    screen.fill(WHITE)

    pygame.draw.circle(screen, BLUE, (x, y), r)

    pygame.display.update()

    is_pressed = pygame.key.get_pressed()

    if is_pressed[pygame.K_LEFT]:
        x -= step

    if is_pressed[pygame.K_RIGHT]:
        x += step

    if is_pressed[pygame.K_UP]:
        y -= step

    if is_pressed[pygame.K_DOWN]:
        y += step

    pygame.display.set_caption(f"move_circle [{int(clock.get_fps())} fps]")

    clock.tick(FPS)
