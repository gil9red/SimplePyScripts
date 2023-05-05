#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Кривая Коха

"""


# Оригинал: https://ru.wikipedia.org/wiki/Кривая_Коха
# <?php
#     $i = 4;
#
#     $image = imagecreatetruecolor(600, 200);
#     imagefilledrectangle($image, 0, 0, imagesx($image) - 1, imagesy($image) - 1,
#                          imagecolorresolve($image, 255, 255, 255));
#     $color = imagecolorresolve($image, 0, 0, 0);
#
#     drawKoch($image, 0, imagesy($image) - 1, imagesx($image), imagesy($image) - 1, $i, $color);
#
#     /**
#      * Draws koch curve between two points.
#      * @return void
#      */
#     function drawKoch($image, $xa, $ya, $xe, $ye, $i, $color) {
#         if($i == 0)
#             imageline($image, $xa, $ya, $xe, $ye, $color);
#         else {
#             //       C
#             //      / \
#             // A---B   D---E
#
#             $xb = $xa + ($xe - $xa) * 1/3;
#             $yb = $ya + ($ye - $ya) * 1/3;
#
#             $xd = $xa + ($xe - $xa) * 2/3;
#             $yd = $ya + ($ye - $ya) * 2/3;
#
#             $cos60 = 0.5;
#             $sin60 = -0.866;
#             $xc = $xb + ($xd - $xb) * $cos60 - $sin60 * ($yd - $yb);
#             $yc = $yb + ($xd - $xb) * $sin60 + $cos60 * ($yd - $yb);
#
#             drawKoch($image, $xa, $ya, $xb, $yb, $i - 1, $color);
#             drawKoch($image, $xb, $yb, $xc, $yc, $i - 1, $color);
#             drawKoch($image, $xc, $yc, $xd, $yd, $i - 1, $color);
#             drawKoch($image, $xd, $yd, $xe, $ye, $i - 1, $color);
#         }
#     }
#
#     header('Content-type: image/png');
#     imagepng($image);
#     imagedestroy($image);
# ?>


from PIL import Image, ImageDraw


def draw_koch(draw, xa, ya, xe, ye, n):
    """
    Draws koch curve between two points.

    """

    if n == 0:
        draw.line((xa, ya, xe, ye), fill="black")
    else:
        #       C
        #      / \
        # A---B   D---E

        xb = xa + (xe - xa) * 1 / 3
        yb = ya + (ye - ya) * 1 / 3

        xd = xa + (xe - xa) * 2 / 3
        yd = ya + (ye - ya) * 2 / 3

        cos60 = 0.5
        sin60 = -0.866
        xc = xb + (xd - xb) * cos60 - sin60 * (yd - yb)
        yc = yb + (xd - xb) * sin60 + cos60 * (yd - yb)

        draw_koch(draw, xa, ya, xb, yb, n - 1)
        draw_koch(draw, xb, yb, xc, yc, n - 1)
        draw_koch(draw, xc, yc, xd, yd, n - 1)
        draw_koch(draw, xd, yd, xe, ye, n - 1)


if __name__ == "__main__":
    img = Image.new("RGB", (600, 200), "white")

    step = 4
    draw_koch(ImageDraw.Draw(img), 0, img.height - 1, img.width, img.height - 1, step)

    img.save("img.png")
