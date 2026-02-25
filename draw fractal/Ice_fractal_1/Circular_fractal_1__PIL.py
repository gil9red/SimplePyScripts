#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Ледяной фрактал 1 / Ice fractal 1

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses CRT, GraphABC;
#
# procedure Draw(x, y, l, u : Real; t : Integer);
#
# procedure Draw2(Var x, y: Real; l, u : Real; t : Integer);
# begin
#     Draw(x, y, l, u, t);
#     x := x + l*cos(u);
#     y := y - l*sin(u);
# end;
# begin
#     if t > 0 then
#     begin
#         l := l*0.5;
#         Draw2(x, y, l, u, t-1);
#         Draw2(x, y, l*0.8, u+pi/2, t-1);
#         Draw2(x, y, l*0.8, u-pi/2, t-1);
#         Draw2(x, y, l, u, t-1)
#     end
#     else
#         Line(Round(x), Round(y), Round(x+cos(u)*l), Round(y-sin(u)*l))
# end;
#
# begin
#   SetWindowCaption('Фракталы: Ледяной фрактал 1');
#   SetWindowSize(420,420);
#     Draw(410, 10, 400, -pi, 5);
#     Draw(10, 410, 400, 0, 5);
#     Draw(10, 10, 400, -pi/2, 5);
#     Draw(410, 410, 400, pi/2, 5);
#     ReadKey
# end.


from math import *
from PIL import Image, ImageDraw


def draw_ice_fractal_1(draw_by_image, step) -> None:
    def draw2(x, y, l, u, t):
        draw(x, y, l, u, t)
        return x + l * cos(u), y - l * sin(u)

    def draw(x, y, l, u, t) -> None:
        if t > 0:
            l *= 0.5
            x, y = draw2(x, y, l, u, t - 1)
            x, y = draw2(x, y, l * 0.8, u + pi / 2, t - 1)
            x, y = draw2(x, y, l * 0.8, u - pi / 2, t - 1)
            _, _ = draw2(x, y, l, u, t - 1)

        else:
            draw_by_image.line((x, y, x + cos(u) * l, y - sin(u) * l), "black")

    draw(410, 10, 400, -pi, step)
    draw(10, 410, 400, 0, step)
    draw(10, 10, 400, -pi / 2, step)
    draw(410, 410, 400, pi / 2, step)


if __name__ == "__main__":
    img = Image.new("RGB", (420, 420), "white")

    step = 5
    draw_ice_fractal_1(ImageDraw.Draw(img), step)

    img.save("img.png")
