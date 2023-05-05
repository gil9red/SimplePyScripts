#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Папоротник 2 / Fern 2

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses GraphABC;
# const
#     min = 1;
#
# procedure lineto1(x, y : Integer; l, u : real);
# begin
#     Line(x, y, Round(x + l * cos(u)), Round(y - l * sin(u)));
# end;
#
# procedure Draw(x, y : Integer; l, u : real);
#
# begin
#     if l > min then
#     begin
#         lineto1(x, y, l, u);
#         x := Round(x + l * cos(u));
#         y := Round(y - l * sin(u));
#         Draw(x, y, l*0.4, u - 14*pi/30);
#         Draw(x, y, l*0.4, u + 14*pi/30);
#         Draw(x, y, l*0.7, u + pi/30);
#     end;
# end;
#
# begin
#      SetWindowCaption('Фракталы: Папоротник');
#    SetWindowSize(730,500);
#    ClearWindow;
#     Draw(320, 460, 140, pi/2)
# end.


from math import *
from PIL import Image, ImageDraw


def draw_fern_2(draw_by_image):
    def line_to(x, y, l, u):
        draw_by_image.line((x, y, x + l * cos(u), y - l * sin(u)), "black")

    def draw(x, y, l, u):
        if l > 1:
            line_to(x, y, l, u)

            x += l * cos(u)
            y -= l * sin(u)

            draw(x, y, l * 0.4, u - 14 * pi / 30)
            draw(x, y, l * 0.4, u + 14 * pi / 30)
            draw(x, y, l * 0.7, u + pi / 30)

    draw(320, 460, 140, pi / 2)


if __name__ == "__main__":
    img = Image.new("RGB", (730, 500), "white")

    draw_fern_2(ImageDraw.Draw(img))

    img.save("img.png")
