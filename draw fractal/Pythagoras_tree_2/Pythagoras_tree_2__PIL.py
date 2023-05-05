#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Дерево Пифагора 2 / Pythagoras Tree 2

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses GraphABC;
# const
#     max = 3;
#
# procedure LineTo1(x, y : Integer; l, u : Real);
# begin
#     Line(x, y, Round(x + l * cos(u)), Round(y - l * sin(u)));
# end;
#
# procedure Draw(x, y : Integer; l, u : real);
# begin
#     if l > max then
#     begin
#         l := l * 0.7;
#         LineTo1(x, y, l, u);
#         x := Round(x + l * cos(u));
#         y := Round(y - l * sin(u));
#         Draw(x, y, l, u + pi / 4); {Угол поворота 1}
#         Draw(x, y, l, u - pi / 6); {Угол поворота 2}
#     end;
# end;
#
# begin
#    SetWindowCaption('Фракталы: Дерево Пифагора');
#    SetWindowSize(730,500);
#    ClearWindow;
#    Draw(320, 460, 200, pi/2)
# end.


from math import *
from PIL import Image, ImageDraw


def draw_pythagoras_tree_2(draw_by_image):
    def line_to(x, y, l, u):
        draw_by_image.line((x, y, x + l * cos(u), y - l * sin(u)), "black")

    def draw(x, y, l, u):
        if l > 3:
            l *= 0.7
            line_to(x, y, l, u)

            x += l * cos(u)
            y -= l * sin(u)

            draw(x, y, l, u + pi / 4)  # Угол поворота 1
            draw(x, y, l, u - pi / 6)  # Угол поворота 2

    draw(320, 460, 200, pi / 2)


if __name__ == "__main__":
    img = Image.new("RGB", (730, 500), "white")

    draw_pythagoras_tree_2(ImageDraw.Draw(img))

    img.save("img.png")
