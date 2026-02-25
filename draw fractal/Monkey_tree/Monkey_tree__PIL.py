#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Обезьянье дерево / Monkey tree

"""


# Оригинал: http://www.cyberforum.ru/pascalabc/thread994987.html
# uses GraphABC;
#
# procedure Draw(x, y, l, u : Real; t, q,s : Integer);
#
# procedure Draw2(Var x, y: Real; l, u : Real; t, q, s : Integer);
# begin
#     Draw(x, y, l, u, t, q, s);
#     x := x + l*cos(u);
#     y := y - l*sin(u);
# end;
#
# begin
#     if t > 0 then
#     begin
#         if q = 1 then
#         begin
#             x := x + l*cos(u);
#             y := y - l*sin(u);
#             s := -s;
#             u := u + pi
#         end
#         else if q = 3 then
#         begin
#             x := x + l*cos(u);
#             y := y - l*sin(u);
#             s := s;
#             u := u + pi
#         end
#         else if q = 2 then
#         begin
#             s:=-s
#         end
#         else if q = 0 then
#         begin
#             s := s
#         end;
#         l := l/3;
#         Draw2(x, y, l,           u+s*pi/3,   t-1, 2,s);
#         Draw2(x, y, l,           u+s*pi/3,   t-1, 1,s);
#         Draw2(x, y, l,           u,          t-1, 0,s);
#         Draw2(x, y, l,           u-s*pi/3,   t-1, 1,s);
#         Draw2(x, y, l*sqrt(3)/3, u-s*7*pi/6, t-1, 1,s);
#         Draw2(x, y, l*sqrt(3)/3, u-s*7*pi/6, t-1, 2,s);
#         Draw2(x, y, l*sqrt(3)/3, u-s*5*pi/6, t-1, 3,s);
#         Draw2(x, y, l*sqrt(3)/3, u-s*pi/2,   t-1, 3,s);
#         Draw2(x, y, l*sqrt(3)/3, u-s*pi/2,   t-1, 0,s);
#         Draw2(x, y, l,           u,          t-1, 3,s);
#         Draw2(x, y, l,           u,          t-1, 0,s);
#
#     end
#     else
#         Line(Round(x), Round(y), Round(x + cos(u)*l), Round(y - sin(u)*l));
# end;
#
# begin
#     SetWindowCaption('Фракталы: Обезьянье дерево');
#   SetWindowSize(520,500);
#   ClearWindow;
#     Draw(50, 365, 430, 0, 3, 0, 1)
# end.


from math import *
from PIL import Image, ImageDraw


def draw_monkey_tree(draw_by_image) -> None:
    def draw2(x, y, l, u, t, q, s):
        draw(x, y, l, u, t, q, s)
        return x + l * cos(u), y - l * sin(u)

    def draw(x, y, l, u, t, q, s) -> None:
        if t > 0:
            if q == 1:
                x += l * cos(u)
                y -= l * sin(u)
                s = -s
                u = u + pi

            elif q == 3:
                x += l * cos(u)
                y -= l * sin(u)
                s = s
                u = u + pi

            elif q == 2:
                s = -s

            elif q == 0:
                s = s

            l /= 3
            x, y = draw2(x, y, l, u + s * pi / 3, t - 1, 2, s)
            x, y = draw2(x, y, l, u + s * pi / 3, t - 1, 1, s)
            x, y = draw2(x, y, l, u, t - 1, 0, s)
            x, y = draw2(x, y, l, u - s * pi / 3, t - 1, 1, s)
            x, y = draw2(x, y, l * sqrt(3) / 3, u - s * 7 * pi / 6, t - 1, 1, s)
            x, y = draw2(x, y, l * sqrt(3) / 3, u - s * 7 * pi / 6, t - 1, 2, s)
            x, y = draw2(x, y, l * sqrt(3) / 3, u - s * 5 * pi / 6, t - 1, 3, s)
            x, y = draw2(x, y, l * sqrt(3) / 3, u - s * pi / 2, t - 1, 3, s)
            x, y = draw2(x, y, l * sqrt(3) / 3, u - s * pi / 2, t - 1, 0, s)
            x, y = draw2(x, y, l, u, t - 1, 3, s)
            _, _ = draw2(x, y, l, u, t - 1, 0, s)

        else:
            draw_by_image.line((x, y, x + cos(u) * l, y - sin(u) * l), "black")

    draw(50, 365, 430, 0, 3, 0, 1)


if __name__ == "__main__":
    img = Image.new("RGB", (520, 500), "white")

    draw_monkey_tree(ImageDraw.Draw(img))

    img.save("img.png")
