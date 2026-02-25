#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Кривая Леви

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses GraphABC;
#
# procedure Draw;
# const iter = 50000;
# var
#     t, x, y, p : Real;
#     k : LongInt;
#     mx, my, rad : Integer;
# begin
#     mx := 200;
#     my := 300;
#     rad := 250;
#     Randomize;
#     x := 0.0;
#     y := 0.0;
#     for k := 1 to iter do
#     begin
#         p := Random;
#         t := x;
#         if p <= 1/2 then
#         begin
#             x := 0.5*x - 0.5*y;
#             y := 0.5*t + 0.5*y;
#         end
#         else
#         begin
#             x := 0.5*x + 0.5*y + 0.5;
#             y := -0.5*t + 0.5*y + 0.5;
#         end;
#         PutPixel(mx + Round(rad * x), my - Round(rad * y), clBlue);
#     end;
# end;
#
# begin
#     SetWindowCaption('Фракталы: Кривая Леви');
#   SetWindowSize(650,450);
#   ClearWindow;
#     Draw
# end.


import random
from PIL import Image, ImageDraw


def draw_levy(draw) -> None:
    iter = 50000

    mx = 200
    my = 300
    rad = 250

    x = 0.0
    y = 0.0

    for k in range(iter):
        p = random.random()
        t = x
        if p <= 1 / 2:
            x = 0.5 * x - 0.5 * y
            y = 0.5 * t + 0.5 * y
        else:
            x = 0.5 * x + 0.5 * y + 0.5
            y = -0.5 * t + 0.5 * y + 0.5

        draw.point((mx + rad * x, my - rad * y), "blue")


if __name__ == "__main__":
    img = Image.new("RGB", (650, 450), "white")

    step = 10

    draw_levy(ImageDraw.Draw(img))

    img.save("img.png")
