#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Круговой фрактал / Circular fractal

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses GraphABC;
# procedure Draw (x,y,size:integer);
#  var min,m,n:integer;
#      i,s1,s2:integer;
#  begin
#   min:=1;m:=6;n:=3;
#   if size > min
#    then
#     begin
#      s1:=round(size/n );
#      s2:=round(size*(n-1)/n );
#      for i:= 1 to  m do
#       Draw ( x - round ( s2*sin ( 2*pi/m*i ) ) , y + round ( s2*cos ( 2*pi/m*i ) ) , s1 );
#      Draw ( x, y, s1 );
#     end;
#   ellipse ( x - size, y - size, x + size, y + size );
#  end;
# begin
#   SetBrushStyle(bsclear);
#   SetWindowTitle('Фракталы: круговой фрактал');
#   Draw(320,240,200);
# end.


from math import *
from PIL import Image, ImageDraw


def draw_circular_fractal(draw_by_image, x, y, size):
    m = 6
    n = 3

    if size > 1:
        s1 = size // n
        s2 = size * (n - 1) // n

        for i in range(m):
            draw_circular_fractal(
                draw_by_image,
                x - s2 * sin(2 * pi / m * i),
                y + s2 * cos(2 * pi / m * i),
                s1,
            )

        draw_circular_fractal(draw_by_image, x, y, s1)

    bbox = (x - size, y - size, x + size, y + size)
    draw_by_image.ellipse(bbox, outline="black")


if __name__ == "__main__":
    img = Image.new("RGB", (320 * 2, 240 * 2), "white")

    draw_circular_fractal(ImageDraw.Draw(img), 320, 240, 200)

    img.save("img.png")
