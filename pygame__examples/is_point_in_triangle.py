#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
import sys

import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


@dataclass
class Point:
    x: float
    y: float


def get_triangle_area(a: Point, b: Point, c: Point) -> float:
    return abs((a.x - c.x) * (b.y - c.y) + (b.x - c.x) * (c.y - a.y))


def is_point_in_triangle(a: Point, b: Point, c: Point, p: Point) -> bool:
    tr_area = get_triangle_area(a, b, c)  # Площадь основного треугольника

    tr_area2 = get_triangle_area(
        a, b, p
    )  # Площади треугольника, образованного из 2 точек основного
    tr_area3 = get_triangle_area(
        a, p, c
    )  # и точки, которая проверяется на принадлежность
    tr_area4 = get_triangle_area(b, p, c)  # к треугольнику

    # Если площади образованных треугольников равны, то точка в треугольнике
    return tr_area == tr_area2 + tr_area3 + tr_area4


pygame.init()

color = BLACK
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
mouse_pos = Point(0, 0)

# Triangle
a, b, c = Point(100, 100), Point(100, 400), Point(500, 500)

fnt = pygame.font.Font(None, 40)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos.x, mouse_pos.y = event.pos
            break

    screen.fill(WHITE)

    # This draws a triangle using the polygon command
    pygame.draw.polygon(screen, BLACK, [[a.x, a.y], [b.x, b.y], [c.x, c.y]], 5)

    if is_point_in_triangle(a, b, c, mouse_pos):
        color = BLACK
    else:
        color = WHITE

    text = fnt.render("Collision!", True, color)
    screen.blit(text, (260, 20))

    pygame.display.update()
    clock.tick(60)
