#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

import pygame

# SOURCE: https://raw.githubusercontent.com/cosmologicon/pygame-text/master/ptext.py
import ptext


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


pygame.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

surf = pygame.Surface((100, 100))
surf.fill(BLACK)
rect = surf.get_rect()


text = """\
Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore 
magna aliqua. Ut enim ad minim veniam, quis nostrud 
exercitation ullamco laboris nisi ut aliquip ex ea 
commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate 
velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, 
sunt in culpa qui officia deserunt mollit anim id 
est laborum.
"""


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            rect.center = event.pos
            break

    screen.fill(WHITE)
    screen.blit(surf, rect)
    ptext.draw(text, (10, 10), color=WHITE, fontsize=30)

    pygame.display.update()
    clock.tick(60)
