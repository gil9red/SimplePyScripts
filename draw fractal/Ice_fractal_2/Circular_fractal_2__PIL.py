#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Ледяной фрактал 2 / Ice fractal 2

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses CRT, GraphABC;
#
# procedure Draw(x, y, l, u : Real; t : Integer);
# procedure Draw2(Var x, y: Real; l, u : Real; t : Integer);
#
# begin
#     Draw(x, y, l, u, t);
#     x := x + l*cos(u);
#     y := y - l*sin(u);
# end;
#
# begin
#     if t > 0 then
#     begin
#         l := l*0.5;
#         Draw2(x, y, l, u, t-1);
#         Draw2(x, y, l*0.45, u+2*pi/3, t-1);
#         Draw2(x, y, l*0.45, u-pi/3, t-1);
#         Draw2(x, y, l*0.45, u+pi/3, t-1);
#         Draw2(x, y, l*0.45, u-2*pi/3, t-1);
#         Draw2(x, y, l, u, t-1)
#     end
#     else
#         Line(Round(x), Round(y), Round(x+cos(u)*l), Round(y-sin(u)*l))
# end;
#
# begin
#   SetWindowCaption('Фракталы: Ледяной фрактал 2');
#   SetWindowSize(420,420);
#     Draw(210, 8, 400, -2*pi/3, 3);
#     Draw(10, 354, 400, 0, 3);
#     Draw(410, 354, 400, 2*pi/3, 3);
#     ReadKey
# end.


from math import *
from PIL import Image, ImageDraw


def draw_ice_fractal_2(draw_by_image, step):
    def draw2(x, y, l, u, t):
        draw(x, y, l, u, t)
        return x + l * cos(u), y - l * sin(u)

    def draw(x, y, l, u, t):
        if t > 0:
            l *= 0.5
            x, y = draw2(x, y, l, u, t - 1)
            x, y = draw2(x, y, l * 0.45, u + 2 * pi / 3, t - 1)
            x, y = draw2(x, y, l * 0.45, u - pi / 3, t - 1)
            x, y = draw2(x, y, l * 0.45, u + pi / 3, t - 1)
            x, y = draw2(x, y, l * 0.45, u - 2 * pi / 3, t - 1)
            _, _ = draw2(x, y, l, u, t - 1)

        else:
            draw_by_image.line((x, y, x + cos(u) * l, y - sin(u) * l), "black")

    draw(210, 8, 400, -2 * pi / 3, step)
    draw(10, 354, 400, 0, step)
    draw(410, 354, 400, 2 * pi / 3, step)


if __name__ == "__main__":
    img = Image.new("RGB", (420, 420), "white")

    step = 6
    draw_ice_fractal_2(ImageDraw.Draw(img), step)

    img.save("img.png")
