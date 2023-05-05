#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Ковёр Серпинского / Sierpinski_carpet

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# Uses CRT, GraphABC;
# Const Z = 6; {Глубина фрактала}
# Var
#    x1, y1, x2, y2, x3, y3: Real;
#
# Procedure Serp(x1, y1, x2, y2: Real; n: Integer);
# Var
#    x1n, y1n, x2n, y2n: Real;
# Begin
#      If  n > 0  Then
#      Begin
#           x1n := 2*x1/3 + x2 / 3;
#           x2n := x1/3 + 2*x2 / 3;
#           y1n := 2*y1/3 + y2 / 3;
#           y2n := y1/3+2*y2 / 3;
#           Rectangle(Round(x1n), Round(y1n), Round(x2n), Round(y2n));
#           Serp(x1, y1, x1n, y1n, n-1);
#           Serp(x1n, y1, x2n, y1n, n-1);
#           Serp(x2n, y1, x2, y1n, n-1);
#           Serp(x1, y1n, x1n, y2n, n-1);
#           Serp(x2n, y1n, x2, y2n, n-1);
#           Serp(x1, y2n, x1n, y2, n-1);
#           Serp(x1n, y2n, x2n, y2, n-1);
#           Serp(x2n, y2n, x2, y2, n-1)
#      End
# End;
# Begin
#      SetWindowCaption('Фракталы: Ковер Серпинского');
#      SetWindowSize(500,500);
#      ClearWindow;
#      Rectangle(20, 20, 460, 460);
#      Serp(20, 20, 460, 460, Z);
#      Repeat Until Keypressed
# End.


from PIL import Image, ImageDraw


def draw_sierpinski_carpet(draw_by_image, Z):
    def serp(x1, y1, x2, y2, n):
        if n > 0:
            x1n = 2 * x1 / 3 + x2 / 3
            x2n = x1 / 3 + 2 * x2 / 3
            y1n = 2 * y1 / 3 + y2 / 3
            y2n = y1 / 3 + 2 * y2 / 3

            draw_by_image.rectangle((x1n, y1n, x2n, y2n), fill="white", outline="black")

            serp(x1, y1, x1n, y1n, n - 1)
            serp(x1n, y1, x2n, y1n, n - 1)
            serp(x2n, y1, x2, y1n, n - 1)
            serp(x1, y1n, x1n, y2n, n - 1)
            serp(x2n, y1n, x2, y2n, n - 1)
            serp(x1, y2n, x1n, y2, n - 1)
            serp(x1n, y2n, x2n, y2, n - 1)
            serp(x2n, y2n, x2, y2, n - 1)

    draw_by_image.rectangle((20, 20, 460, 460), fill="white", outline="black")
    serp(20, 20, 460, 460, Z)


if __name__ == "__main__":
    img = Image.new("RGB", (500, 500), "white")

    # Глубина фрактала
    Z = 4

    draw_sierpinski_carpet(ImageDraw.Draw(img), Z)

    img.save("img.png")
