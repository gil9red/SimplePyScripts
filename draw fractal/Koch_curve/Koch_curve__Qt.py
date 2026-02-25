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


def draw_koch(painter, xa, ya, xe, ye, n) -> None:
    """
    Draws koch curve between two points.

    """

    if n == 0:
        painter.drawLine(xa, ya, xe, ye)
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

        draw_koch(painter, xa, ya, xb, yb, n - 1)
        draw_koch(painter, xb, yb, xc, yc, n - 1)
        draw_koch(painter, xc, yc, xd, yd, n - 1)
        draw_koch(painter, xd, yd, xe, ye, n - 1)


try:
    from PyQt5.QtGui import QImage, QPainter
    from PyQt5.QtCore import Qt

except ImportError:
    try:
        from PyQt4.QtGui import QImage, QPainter
        from PyQt4.QtCore import Qt

    except ImportError:
        from PySide.QtGui import QImage, QPainter
        from PySide.QtCore import Qt


if __name__ == "__main__":
    img = QImage(600, 200, QImage.Format_RGB16)
    img.fill(Qt.white)

    step = 4

    painter = QPainter(img)
    painter.setPen(Qt.black)
    draw_koch(painter, 0, img.height() - 1, img.width(), img.height() - 1, step)

    img.save("img.png")
