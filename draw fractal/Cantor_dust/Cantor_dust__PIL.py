#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Канторова пыль / Cantor dust

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses GraphABC;
# const
#     min = 1;
#
# procedure Draw(x, y : Real; Size : Real);
# var
#     s : Real;
#
# begin
#     if size > min then
#     begin
#         s := size / 3;
#         Draw(x, y + 20, s);
#         Draw(x + s * 2, y + 20, s);
#     end;
#     Rectangle(Round(x), Round(y), Round(x + size), Round(y + 5))
# end;
#
# begin
#     SetWindowCaption('Фракталы: Канторова пыль');
#   SetWindowSize(520,160);
#   ClearWindow;
#     Draw(10,30,500)
# end.


from PIL import Image, ImageDraw


def draw_cantor_dust(draw_by_image):
    def draw(x, y, size):
        if size > 1:
            s = size / 3
            draw(x, y + 20, s)
            draw(x + s * 2, y + 20, s)

        draw_by_image.rectangle((x, y, x + size, y + 5), "black")

    draw(10, 30, 500)


if __name__ == "__main__":
    img = Image.new("RGB", (520, 160), "white")

    draw_cantor_dust(ImageDraw.Draw(img))

    img.save("img.png")
