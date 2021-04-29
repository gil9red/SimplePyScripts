#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

# pip install pygame
# pip install pygametext
import pygame
import pygametext

running = True

pygame.init()

screen = pygame.display.set_mode((640, 360))
clock = pygame.time.Clock()

pgt = pygametext.PGT(screen)  # Define pygametext object.

pgt.button(10, 10, 100, 50, (255, 0, 0), "Hello!", (0, 0, 0), print, "Hello World!", 0)  # Add pgt Button
pgt.button(120, 10, 100, 50, (255, 255, 0), "Bye bye", (0, 0, 0), print, "Goodbye World!", 0)  # Add pgt Button
pgt.text(10, 70, "Simple pygametext example.", (0, 120, 0), 20, 0)  # Add pgt Text


def update():  # Update & Eventd
    global running

    events = pygame.event.get()

    pgt.update(events, 0)  # Update all pgt elements from layer 0. Takes events arg to process some elements.

    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()


def draw():
    screen.fill((255, 255, 255))  # Clear screen
    pgt.draw()  # Draw all pgt elements from layer 0

    pygame.display.flip()


while running:
    update()
    draw()
    clock.tick(60)
