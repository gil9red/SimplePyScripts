#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://www.nerdparadise.com/programming/pygame/part1


import math
import sys

# pip install pygame
import pygame


pygame.init()

joystick_count = pygame.joystick.get_count()
if joystick_count:
    # Use joystick #0 and initialize it
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    # No joysticks!
    print("Error, I didn't find any joysticks.")
    sys.exit()

screen = pygame.display.set_mode((400, 300))

game_active = True
is_blue = True
x = 100
y = 100

clock = pygame.time.Clock()

while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False
            break

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue
            break

        if event.type == pygame.JOYBUTTONDOWN:
            is_blue = not is_blue
            break

    # JOYHATMOTION
    hat_x, hat_y = joystick.get_hat(0)

    # JOYAXISMOTION
    # Left joystick axes
    # .get_axis(2) -- Trigger axes
    # .get_axis(3) / .get_axis(4) -- Right joystick axes
    axis_x, axis_y = joystick.get_axis(0), joystick.get_axis(1)
    axis_x = math.floor(axis_x * 1000)
    axis_y = math.floor(axis_y * 1000)

    pressed = pygame.key.get_pressed()

    # If Esc clicked
    if pressed[pygame.K_ESCAPE] or not game_active:
        break

    if pressed[pygame.K_UP] or pressed[pygame.K_w] or hat_y == 1 or axis_y < -500:
        y -= 3

    if pressed[pygame.K_DOWN] or pressed[pygame.K_s] or hat_y == -1 or axis_y > 500:
        y += 3

    if pressed[pygame.K_LEFT] or pressed[pygame.K_a] or hat_x == -1 or axis_x < -500:
        x -= 3

    if pressed[pygame.K_RIGHT] or pressed[pygame.K_d] or hat_x == 1 or axis_x > 500:
        x += 3

    screen.fill((0, 0, 0))

    color = (0, 128, 255) if is_blue else (255, 100, 0)
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))

    pygame.display.flip()

    pygame.display.set_caption("move_rect [{} fps]".format(int(clock.get_fps())))

    # will block execution until 1/60 seconds have passed
    # since the previous time clock.tick was called.
    clock.tick(60)
