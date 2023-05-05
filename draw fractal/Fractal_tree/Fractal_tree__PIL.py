#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Фрактальное дерево / Fractal tree

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# Uses GraphABC;
# Procedure Tree(x, y: Integer; a: Real; l: Integer);
# Var
#    x1, y1: Integer;
#    p, s : Integer;
#    i : Integer;
#    a1 : Real;
# Begin
#      If l < 8 Then
#      exit;
#      x1 := Round(x + l*cos(a));
#      y1 := Round(y + l*sin(a));
#      If l > 100 Then p := 100 Else p := l;
#      If p < 40 Then
#      Begin
#           {Генерация листьев}
#           If Random > 0.5 Then SetPenColor(clLime) Else SetPenColor(clGreen);
#           For i := 0 To 3 Do
#               Line(x + i, y, x1, y1)
#      End
#      Else
#      Begin
#           {Генерация веток}
#           SetPenColor(clBrown);
#           For i := 0 To (p div 6) Do
#               Line(x + i - (p div 12), y, x1, y1)
#      End;
#      {Следующие ветки}
#      For i := 0 To 9 - Random(9) Do
#      Begin
#           s := Random(l - l div 6) + (l div 6);
#           a1 := a + 1.6 * (0.5 - Random); {Угол наклона веток}
#           x1 := Round(x + s * cos(a));
#           y1 := Round(y + s * sin(a));
#           Tree(x1, y1, a1, p - 5 - Random(30)) {Чем меньше вычитаем, тем пышнее дерево}
#      End
# End;
#
# {Основная программа}
# Begin
#   SetWindowCaption('Фрактальное дерево');
#   SetWindowSize(700,600);
#   Randomize;
#   Tree(350, 580, 3*pi/2, 200)
# End.


import random
from math import *

from PIL import Image, ImageDraw


def draw_fractal_tree(draw_by_image, x, y, a, l):
    if l < 8:
        return

    x1 = x + l * cos(a)
    y1 = y + l * sin(a)
    p = 100 if l > 100 else l

    if p < 40:
        # Генерация листьев
        color = "lime" if random.random() > 0.5 else "green"

        for i in range(3):
            draw_by_image.line((x + i, y, x1, y1), color)
    else:
        # Генерация веток
        color = "brown"

        for i in range(p // 6):
            draw_by_image.line((x + i - (p / 12), y, x1, y1), color)

    # Следующие ветки
    for i in range(9 - random.randrange(9)):
        s = random.randrange(l - l // 6) + (l / 6)

        # Угол наклона веток
        a1 = a + 1.6 * (0.5 - random.random())
        x1 = x + s * cos(a)
        y1 = y + s * sin(a)

        # Чем меньше вычитаем, тем пышнее дерево
        draw_fractal_tree(draw_by_image, x1, y1, a1, p - 5 - random.randrange(30))


if __name__ == "__main__":
    img = Image.new("RGB", (700, 600), "white")

    draw_fractal_tree(ImageDraw.Draw(img), 350, 580, 3 * pi / 2, 200)

    img.save("img.png")
