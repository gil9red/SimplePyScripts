#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Папоротник / Fern

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses GraphABC,Utils;
#
# const
#   n=255;
#   max=10;
#
# var
#   x,y,x1,y1,cx,cy: real;
#   i,ix,iy: integer;
# // z=z^2+c
# begin
#   SetWindowCaption('Фракталы: папоротник');
#   SetWindowSize(300,300);
#   cx:=0.251;
#   cy:=0.95;
#   for ix:=0 to WindowWidth-1 do
#   for iy:=0 to WindowHeight-1 do
#   begin
#     x:=0.001*(ix-200);
#     y:=0.001*(iy-150);
#     for i:=1 to n do
#     begin
#       x1:=0.5*x*x-0.88*y*y+cx;
#       y1:=x*y+cy;
#       if (x1>max) or (y1>max) then break;
#       x:=x1;
#       y:=y1;
#     end;
#     if i>=n then SetPixel(ix,iy,clGreen)
#       else SetPixel(ix,iy,RGB(255-i,255,255-i));
#   end;
#   writeln('Время расчета = ',Milliseconds/1000,' с');
# end.


from PIL import Image, ImageDraw


def draw_fern(draw_by_image, width, height):
    n = 255

    cx = 0.251
    cy = 0.95

    for ix in range(width):
        for iy in range(height):
            x = 0.001 * (ix - 200)
            y = 0.001 * (iy - 150)

            for i in range(n):
                x1 = 0.5 * x * x - 0.88 * y * y + cx
                y1 = x * y + cy
                if x1 > 10 or y1 > 10:
                    break

                x = x1
                y = y1

            color = "green" if i >= n else (255 - i, 255, 255 - i)
            draw_by_image.point((ix, iy), color)


if __name__ == "__main__":
    img = Image.new("RGB", (300, 300), "white")

    draw_fern(ImageDraw.Draw(img), img.width, img.height)

    img.save("img.png")
