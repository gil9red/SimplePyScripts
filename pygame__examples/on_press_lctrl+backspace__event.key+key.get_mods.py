#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pygame


pygame.init()

screen = pygame.display.set_mode((300, 200))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif (
                event.key == pygame.K_BACKSPACE
                and pygame.key.get_mods() & pygame.KMOD_LCTRL
            ):
                print("pressed: LCTRL + BACKSPACE")

pygame.quit()
