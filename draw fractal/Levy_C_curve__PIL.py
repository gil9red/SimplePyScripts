#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Оригинал: https://ru.wikipedia.org/wiki/Кривая_Леви
# <?php
#     $i = 10;
#
#     $image = imagecreatetruecolor(640, 480);
#     imagefilledrectangle($image, 0, 0, imagesx($image) - 1, imagesy($image) - 1,
#             imagecolorresolve($image, 255, 255, 255));
#     $color = imagecolorresolve($image, 0, 0, 0);
#
#     drawLevy($image, imagesx($image) * 3/8, imagesy($image) * 3/8,
#             imagesx($image) * 5/8, imagesy($image) * 5/8, $i, $color);
#
#     /**
#      * Draws levy curve between two points.
#      * @return void
#      */
#     function drawLevy($image, $xa, $ya, $xc, $yc, $i, $color) {
#         if($i == 0)
#             imageline($image, $xa, $ya, $xc, $yc, $color);
#         else {
#             // A---B
#             //     |
#             //     C
#             $xb = ($xa + $xc) / 2 + ($yc - $ya) / 2;
#             $yb = ($ya + $yc) / 2 - ($xc - $xa) / 2;
#             drawLevy($image, $xa, $ya, $xb, $yb, $i - 1, $color);
#             drawLevy($image, $xb, $yb, $xc, $yc, $i - 1, $color);
#         }
#     }
#
#     header('Content-type: image/png');
#     imagepng($image);
#     imagedestroy($image);
# ?>


def draw_levy(draw, xa, ya, xc, yc, n, color):
    """
    Draws levy curve between two points.

    """

    if n == 0:
        draw.line((xa, ya, xc, yc), fill=color)
    else:
        # A---B
        #     |
        #     C
        xb = (xa + xc) / 2 + (yc - ya) / 2
        yb = (ya + yc) / 2 - (xc - xa) / 2

        draw_levy(draw, xa, ya, xb, yb, n - 1, color)
        draw_levy(draw, xb, yb, xc, yc, n - 1, color)


from PIL import Image, ImageDraw


if __name__ == '__main__':
    n = 10

    img = Image.new("RGB", (640, 480), "white")

    draw_levy(ImageDraw.Draw(img),
              img.width * 3/8, img.height * 3/8, img.width * 5/8, img.height * 5/8,
              n, "black")

    img.save('img.png')
