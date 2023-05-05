#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Кривая Минковского

"""


# Оригинал: https://ru.wikipedia.org/wiki/Кривая_Минковского
# <?php
#     $i = 2;
#
#     $image = imagecreatetruecolor(600, 400);
#     imagefilledrectangle($image, 0, 0, imagesx($image) - 1, imagesy($image) - 1,
#             imagecolorresolve($image, 255, 255, 255));
#     $color = imagecolorresolve($image, 0, 0, 0);
#
#     drawMinkowski($image, 0, imagesy($image) / 2, imagesx($image), imagesy($image) / 2, $i, $color);
#
#     /**
#      * Draws minkowski curve between two points.
#      * @return void
#      */
#     function drawMinkowski($image, $xa, $ya, $xi, $yi, $i, $color) {
#         if($i == 0)
#             imageline($image, $xa, $ya, $xi, $yi, $color);
#         else {
#             //     C---D
#             //     |   |
#             // A---B   E   H---I
#             //         |   |
#             //         F---G
#
#             $xb = $xa + ($xn - $xa) * 1/4;
#             $yb = $ya + ($yn - $ya) * 1/4;
#
#             $xe = $xa + ($xn - $xa) * 2/4;
#             $ye = $ya + ($yn - $ya) * 2/4;
#
#             $xh = $xa + ($xn - $xa) * 3/4;
#             $yh = $ya + ($yn - $ya) * 3/4;
#
#             $cos90 = 0;
#             $sin90 = -1;
#             $xc = $xb + ($xe - $xb) * $cos90 - $sin90 * ($ye - $yb);
#             $yc = $yb + ($xe - $xb) * $sin90 + $cos90 * ($ye - $yb);
#
#             $xd = $xc + ($xe - $xb);
#             $yd = $yc + ($ye - $yb);
#
#             $sin90 = 1;
#             $xf = $xe + ($xh - $xe) * $cos90 - $sin90 * ($yh - $ye);
#             $yf = $ye + ($xh - $xe) * $sin90 + $cos90 * ($yh - $ye);
#
#             $xg = $xf + ($xh - $xe);
#             $yg = $yf + ($yh - $ye);
#
#             drawMinkowski($image, $xa, $ya, $xb, $yb, $n - 1, $color);
#             drawMinkowski($image, $xb, $yb, $xc, $yc, $n - 1, $color);
#             drawMinkowski($image, $xc, $yc, $xd, $yd, $n - 1, $color);
#             drawMinkowski($image, $xd, $yd, $xe, $ye, $n - 1, $color);
#             drawMinkowski($image, $xe, $ye, $xf, $yf, $n - 1, $color);
#             drawMinkowski($image, $xf, $yf, $xg, $yg, $n - 1, $color);
#             drawMinkowski($image, $xg, $yg, $xh, $yh, $n - 1, $color);
#             drawMinkowski($image, $xh, $yh, $xi, $yi, $n - 1, $color);
#         }
#     }
#
#     header('Content-type: image/png');
#     imagepng($image);
#     imagedestroy($image);
# ?>


from PIL import Image, ImageDraw


def draw_minkowski(draw, xa, ya, xi, yi, n):
    """
    Draws minkowski curve between two points.

    """

    if n == 0:
        draw.line((xa, ya, xi, yi), fill="black")
    else:
        #     C---D
        #     |   |
        # A---B   E   H---I
        #         |   |
        #         F---G

        xb = xa + (xi - xa) * 1 / 4
        yb = ya + (yi - ya) * 1 / 4

        xe = xa + (xi - xa) * 2 / 4
        ye = ya + (yi - ya) * 2 / 4

        xh = xa + (xi - xa) * 3 / 4
        yh = ya + (yi - ya) * 3 / 4

        cos90 = 0
        sin90 = -1
        xc = xb + (xe - xb) * cos90 - sin90 * (ye - yb)
        yc = yb + (xe - xb) * sin90 + cos90 * (ye - yb)

        xd = xc + (xe - xb)
        yd = yc + (ye - yb)

        sin90 = 1
        xf = xe + (xh - xe) * cos90 - sin90 * (yh - ye)
        yf = ye + (xh - xe) * sin90 + cos90 * (yh - ye)

        xg = xf + (xh - xe)
        yg = yf + (yh - ye)

        draw_minkowski(draw, xa, ya, xb, yb, n - 1)
        draw_minkowski(draw, xb, yb, xc, yc, n - 1)
        draw_minkowski(draw, xc, yc, xd, yd, n - 1)
        draw_minkowski(draw, xd, yd, xe, ye, n - 1)
        draw_minkowski(draw, xe, ye, xf, yf, n - 1)
        draw_minkowski(draw, xf, yf, xg, yg, n - 1)
        draw_minkowski(draw, xg, yg, xh, yh, n - 1)
        draw_minkowski(draw, xh, yh, xi, yi, n - 1)


if __name__ == "__main__":
    img = Image.new("RGB", (600, 400), "white")

    step = 3
    draw_minkowski(
        ImageDraw.Draw(img), 0, img.height / 2, img.width, img.height / 2, step
    )

    img.save("img.png")
