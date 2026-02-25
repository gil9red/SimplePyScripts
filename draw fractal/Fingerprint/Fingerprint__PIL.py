#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Отпечаток пальца / Fingerprint

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses GraphABC;
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
#   SetWindowCaption('Фракталы: отпечаток пальца');
#   SetWindowSize(400,300);
#   cx:=0.1;
#   cy:=+0.17;
#   for ix:=0 to WindowWidth-1 do
#   for iy:=0 to WindowHeight-1 do
#   begin
#     x:=0.005*(ix-200);
#     y:=0.005*(iy-150);
#     for i:=1 to n do
#     begin
#       x1:=x*x-y*y+cx;
#       y1:=x*y+1.4*y+cy;
#       if (x1>max) or (y1>max) then break;
#       x:=x1;
#       y:=y1;
#     end;
#     if i>=n then SetPixel(ix,iy,clRed)
#       else SetPixel(ix,iy,RGB(255,255-i,255-i));
#   end;
# end.


from PIL import Image, ImageDraw


def draw_fingerprint(draw_by_image, width, height) -> None:
    n = 255
    max = 10

    cx = 0.1
    cy = 0.17

    for ix in range(width - 1):
        for iy in range(height - 1):
            x = 0.005 * (ix - 200)
            y = 0.005 * (iy - 150)

            for i in range(n):
                x1 = x * x - y * y + cx
                y1 = x * y + 1.4 * y + cy

                if x1 > max or y1 > max:
                    break

                x = x1
                y = y1

                if i >= n:
                    color = "red"
                else:
                    color = (255, 255 - i, 255 - i)

                draw_by_image.point((ix, iy), color)


if __name__ == "__main__":
    img = Image.new("RGB", (400, 300), "white")

    draw_fingerprint(ImageDraw.Draw(img), img.width, img.height)

    img.save("img.png")
