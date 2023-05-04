#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Множество Аполлона 1 / Apollon Set

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses CRT, GraphABC
# var
#     x, y, a, b: Real
#     r: Real
#     a0, b0: Real
#     a1, b1, a2, b2: Real
#     f1x, f1y: Real
#     x1, y1: Real
#
# begin
#     setwindowcaption('Фракталы: Множество Апполона')
#   setwindowsize(650, 500)
#   clearwindow
#     x = 0.2
#     y = 0.3
#     a = 0
#     b = 0
#     Randomize
#     r = Sqrt(3)
#     while not KeyPressed do
#     begin
#         a = Random
#         a0 = 3*(1+r-x)/(sqr(1+r-x)+sqr(y))-(1+r)/(2+r)
#         b0 = 3*y/(sqr(1+r-x)+sqr(y))
#         if (a <= 1/3) and (a>=0) then
#         begin
#             x1 = a0
#             y1 = b0
#         end
#         a1 = -1/2
#         b1 = r/2
#         a2 = -1/2
#         b2 = -r/2
#         f1x = a0/(sqr(a0)+sqr(b0))
#         f1y = -b0/(sqr(a0)+sqr(b0))
#         if (a <= 2/3) and (a > 1/3) then
#         begin
#             x1 = f1x*a1-f1y*b1
#             y1 = f1x*b1+f1y*a1
#         end
#         if (a <= 3/3) and (a > 2/3) then
#         begin
#             x1 = f1x*a2-f1y*b2
#             y1 = f1x*b2+f1y*a2
#         end
#         x = x1
#         y = y1
#         PutPixel(320+Round(x*50), 240+Round(y*50), clRed)
#     end
#     ReadKey
# end.

import random
from math import *

from PIL import Image, ImageDraw


def draw_apollon_set(draw_by_image, step):
    x = 0.2
    y = 0.3

    r = sqrt(3)

    sqr = lambda x: x * x

    for i in range(step):
        a = random.random()
        a0 = 3 * (1 + r - x) / (sqr(1 + r - x) + sqr(y)) - (1 + r) / (2 + r)
        b0 = 3 * y / (sqr(1 + r - x) + sqr(y))
        if 1 / 3 >= a >= 0:
            x1 = a0
            y1 = b0

        a1 = -1 / 2
        b1 = r / 2
        a2 = -1 / 2
        b2 = -r / 2
        f1x = a0 / (sqr(a0) + sqr(b0))
        f1y = -b0 / (sqr(a0) + sqr(b0))
        if 2 / 3 >= a > 1 / 3:
            x1 = f1x * a1 - f1y * b1
            y1 = f1x * b1 + f1y * a1

        if 3 / 3 >= a > 2 / 3:
            x1 = f1x * a2 - f1y * b2
            y1 = f1x * b2 + f1y * a2

        x = x1
        y = y1

        draw_by_image.point((320 + x * 50, 240 + y * 50), "red")


if __name__ == "__main__":
    img = Image.new("RGB", (650, 500), "white")

    # Каждый step это одна точка
    step = 50000
    draw_apollon_set(ImageDraw.Draw(img), step)

    img.save("img.png")
