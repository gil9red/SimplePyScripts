#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Снежинка Коха

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses CRT, GraphABC;
#
# procedure Draw(x, y, l, u : Real; t : Integer);
#
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
#         l := l/3;
#         Draw2(x, y, l, u, t-1);
#         Draw2(x, y, l, u+pi/3, t-1);
#         Draw2(x, y, l, u-pi/3, t-1);
#         Draw2(x, y, l, u, t-1);
#     end
#     else
#         Line(Round(x), Round(y), Round(x+cos(u)*l), Round(y-sin(u)*l))
# end;
#
# begin
#   SetWindowSize(425,500);
#   SetWindowCaption('Фракталы: Снежинка Коха');
#     Draw(10, 354, 400, pi/3, 4);
#     Draw(410, 354, 400, pi, 4);
#     Draw(210, 8, 400, -pi/3, 4);
#  Repeat Until KeyPressed
# end.


import math
from PIL import Image, ImageDraw


def draw_snowflake_koch(draw_by_image, step):
    """
    Draws koch snowflake.

    """

    def draw(x, y, l, u, t):
        if t == 0:
            draw_by_image.line(
                (x, y, x + math.cos(u) * l, y - math.sin(u) * l), fill="black"
            )
        else:
            l /= 3
            x, y = draw2(x, y, l, u, t - 1)
            x, y = draw2(x, y, l, u + math.pi / 3, t - 1)
            x, y = draw2(x, y, l, u - math.pi / 3, t - 1)
            _, _ = draw2(x, y, l, u, t - 1)

    def draw2(x, y, l, u, t):
        draw(x, y, l, u, t)
        return x + l * math.cos(u), y - l * math.sin(u)

    draw(10, 354, 400, math.pi / 3, step)
    draw(410, 354, 400, math.pi, step)
    draw(210, 8, 400, -math.pi / 3, step)


if __name__ == "__main__":
    img = Image.new("RGB", (425, 500), "white")
    draw_by_image = ImageDraw.Draw(img)

    step = 4
    draw_snowflake_koch(draw_by_image, step)

    img.save("img.png")
