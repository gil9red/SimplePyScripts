#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Снежинка / Snowflake

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses graphABC;
# const k=8;
# var x,y:integer;
# procedure snow (x0,y0,r,n:integer);
# const t=2*pi/k;
# var i,x,y:integer;
# begin
#  for i:=1 to k do
#   begin
#    x:=x0+round(r*cos(i*t));
#    y:=y0-round(r*sin(i*t));
#    line(x0,y0,x,y);
#    if n>1 then snow(x,y,r div 5,n-1);
#   end;
# end;
# begin
# SetWindowSize(500,500);
# SetWindowCaption('Фракталы: что-то похожее на снежинку');
# x:=windowwidth div 2;
# y:=windowheight div 2;
# snow(x,y,180,4);
# end.


from math import *
from PIL import Image, ImageDraw


def draw_snowflake(draw_by_image, width, height, count):
    def draw(x0, y0, r, n):
        t = 2 * pi / count

        for i in range(count):
            x = x0 + r * cos(i * t)
            y = y0 - r * sin(i * t)
            draw_by_image.line((x0, y0, x, y), "black")

            if n > 1:
                draw(x, y, r // 5, n - 1)

    x = width // 2
    y = height // 2
    draw(x, y, 180, 4)


if __name__ == "__main__":
    img = Image.new("RGB", (500, 500), "white")

    # Количество повторений
    count = 8
    draw_snowflake(ImageDraw.Draw(img), img.width, img.height, count)

    img.save("img.png")
