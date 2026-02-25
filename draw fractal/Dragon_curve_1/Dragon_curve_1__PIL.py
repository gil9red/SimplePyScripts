#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Кривая Дракона 1 / Dragon curve 1

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# Uses CRT, GraphABC;
# Const Z= 12; {Glubina Fraktala}
# Procedure ris(x1,y1,x2,y2,k:integer);
# Var xn,yn:integer;
# Begin
#      If k>0 Then
#      Begin
#           xn:=(x1+x2) div 2 +(y2-y1) div 2;
#           yn:=(y1+y2) div 2 -(x2-x1) div 2;
#           ris(x1,y1,xn,yn,k-1);
#           ris(x2,y2,xn,yn,k-1)
#      End
#      Else
#           line(x1,y1,x2,y2)
#
# End;
# {Main program}
# Begin
#      SetWindowCaption('Фракталы: Кривая Дракона');
#      SetWindowSize(700,512);
#      ClearWindow;
#      ris(200,300,500,300,Z);
#      Repeat Until KeyPressed
# End.


from PIL import Image, ImageDraw


def draw_dragon_curve_1(draw_by_image, x1, y1, x2, y2, k) -> None:
    if k > 0:
        xn = (x1 + x2) // 2 + (y2 - y1) // 2
        yn = (y1 + y2) // 2 - (x2 - x1) // 2
        draw_dragon_curve_1(draw_by_image, x1, y1, xn, yn, k - 1)
        draw_dragon_curve_1(draw_by_image, x2, y2, xn, yn, k - 1)

    else:
        draw_by_image.line((x1, y1, x2, y2), "black")


if __name__ == "__main__":
    img = Image.new("RGB", (700, 512), "white")

    # Глубина фрактала
    z = 14
    draw_dragon_curve_1(ImageDraw.Draw(img), 200, 300, 500, 300, z)

    img.save("img.png")
