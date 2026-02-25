#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Кривая Госпера

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# Program Gosper_Curve;
#
# Uses CRT, GraphABC;
#
# Procedure Draw(x, y, l, u : Real; t, q : Integer);
#
# Procedure Draw2(Var x, y: Real; l, u : Real; t, q : Integer);
#
# Begin
#      Draw(x, y, l, u, t, q);
#        x := x + l*cos(u);
#        y := y - l*sin(u)
# End;
#
# Begin
#      If t > 0 Then
#      Begin
#           If q = 1 Then
#           Begin
#                x := x + l*cos(u);
#                      y := y - l*sin(u);
#                      u := u + pi
#           End;
#           u := u - 2*pi/19;
#               l := l/sqrt(7);
#               Draw2(x, y, l, u, t-1, 0);
#               Draw2(x, y, l, u+pi/3, t-1, 1);
#               Draw2(x, y, l, u+pi, t-1, 1);
#           Draw2(x, y, l, u+2*pi/3, t-1, 0);
#           Draw2(x, y, l, u, t-1, 0);
#           Draw2(x, y, l, u, t-1, 0);
#           Draw2(x, y, l, u-pi/3, t-1, 1)
#      End
#      Else
#          Line(Round(x), Round(y), Round(x + cos(u)*l), Round(y -sin(u)*l))
#      End;
#
# Begin
#      SetWindowCaption('Фракталы: Кривая Госпера');
#      SetWindowSize(650,500);
#      ClearWindow;
#      Draw(100, 355, 400, 0, 4, 0);
#      Repeat Until KeyPressed
# End.


import math
from PIL import Image, ImageDraw


def draw_gosper_curve(draw_by_image, step) -> None:
    def draw(x, y, l, u, t, q) -> None:
        if t > 0:
            if q == 1:
                x += l * math.cos(u)
                y -= l * math.sin(u)
                u += math.pi

            u -= 2 * math.pi / 19
            l /= math.sqrt(7)

            x, y = draw2(x, y, l, u, t - 1, 0)
            x, y = draw2(x, y, l, u + math.pi / 3, t - 1, 1)
            x, y = draw2(x, y, l, u + math.pi, t - 1, 1)
            x, y = draw2(x, y, l, u + 2 * math.pi / 3, t - 1, 0)
            x, y = draw2(x, y, l, u, t - 1, 0)
            x, y = draw2(x, y, l, u, t - 1, 0)
            _, _ = draw2(x, y, l, u - math.pi / 3, t - 1, 1)

        else:
            draw_by_image.line(
                (x, y, x + math.cos(u) * l, y - math.sin(u) * l), fill="black"
            )

    def draw2(x, y, l, u, t, q):
        draw(x, y, l, u, t, q)
        return x + l * math.cos(u), y - l * math.sin(u)

    draw(100, 355, 400, 0, step, 0)


if __name__ == "__main__":
    img = Image.new("RGB", (650, 500), "white")
    draw_by_image = ImageDraw.Draw(img)

    step = 4
    draw_gosper_curve(draw_by_image, step)

    img.save("img.png")
