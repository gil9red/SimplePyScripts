#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Треугольник Серпинского / Sierpinski Triangle

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# Uses CRT, GraphABC;
# Const Z = 7; {Глубина фрактала}
#
# Procedure tr(x1, y1, x2, y2, x3, y3: Real);
# Begin
#      Line(Round(x1), Round(y1), Round(x2), Round(y2));
#        Line(Round(x2), Round(y2), Round(x3), Round(y3));
#        Line(Round(x3), Round(y3), Round(x1), Round(y1));
# End;
#
# Procedure draw(x1, y1, x2, y2, x3, y3: Real; n: Integer);
# Var
#    x1n, y1n, x2n, y2n, x3n, y3n : Real;
# Begin
#      If  n > 0  Then
#      Begin
#           x1n := (x1 + x2) / 2;
#           y1n := (y1 + y2) / 2;
#           x2n := (x2 + x3) / 2;
#           y2n := (y2 + y3) / 2;
#           x3n := (x3 + x1) / 2;
#           y3n := (y3 + y1) / 2;
#           tr(x1n, y1n, x2n, y2n, x3n, y3n);
#           draw(x1, y1, x1n, y1n, x3n, y3n, n - 1);
#           draw(x2, y2, x1n, y1n, x2n, y2n, n - 1);
#           draw(x3, y3, x2n, y2n, x3n, y3n, n - 1)
#      End
# End;
# Begin
#      SetWindowCaption('Фракталы: Треугольник Серпинского');
#      SetWindowSize(650,500);
#      ClearWindow;
#      tr(320,10,600,470,40,470);
#        draw(320,10,600,470,40,470,Z);
#      Repeat Until KeyPressed
# End.


from PIL import Image, ImageDraw


def draw_sierpinski_triangle(draw_by_image, Z):
    color = "black"

    def tr(x1, y1, x2, y2, x3, y3):
        draw_by_image.line((x1, y1, x2, y2), color)
        draw_by_image.line((x2, y2, x3, y3), color)
        draw_by_image.line((x3, y3, x1, y1), color)

    def draw(x1, y1, x2, y2, x3, y3, n):
        if n > 0:
            x1n = (x1 + x2) / 2
            y1n = (y1 + y2) / 2
            x2n = (x2 + x3) / 2
            y2n = (y2 + y3) / 2
            x3n = (x3 + x1) / 2
            y3n = (y3 + y1) / 2

            tr(x1n, y1n, x2n, y2n, x3n, y3n)
            draw(x1, y1, x1n, y1n, x3n, y3n, n - 1)
            draw(x2, y2, x1n, y1n, x2n, y2n, n - 1)
            draw(x3, y3, x2n, y2n, x3n, y3n, n - 1)

    tr(320, 10, 600, 470, 40, 470)
    draw(320, 10, 600, 470, 40, 470, Z)


if __name__ == "__main__":
    img = Image.new("RGB", (650, 500), "white")

    # Глубина фрактала
    Z = 6

    draw_sierpinski_triangle(ImageDraw.Draw(img), Z)

    img.save("img.png")
