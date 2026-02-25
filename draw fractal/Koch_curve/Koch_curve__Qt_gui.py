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
    from PyQt5.QtWidgets import (
        QApplication,
        QWidget,
        QLabel,
        QSpinBox,
        QVBoxLayout,
        QSizePolicy,
    )
    from PyQt5.QtGui import QImage, QPixmap, QPainter
    from PyQt5.QtCore import Qt

except ImportError:
    try:
        from PyQt4.QtGui import (
            QImage,
            QPainter,
            QApplication,
            QWidget,
            QLabel,
            QSpinBox,
            QVBoxLayout,
            QSizePolicy,
            QPixmap,
        )
        from PyQt4.QtCore import Qt

    except ImportError:
        from PySide.QtGui import (
            QImage,
            QPainter,
            QApplication,
            QWidget,
            QLabel,
            QSpinBox,
            QVBoxLayout,
            QSizePolicy,
            QPixmap,
        )
        from PySide.QtCore import Qt


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Koch_curve snowflake")

        self.img_label = QLabel()
        self.img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.step_spinbox = QSpinBox()
        self.step_spinbox.setRange(0, 15)
        self.step_spinbox.setValue(4)
        self.step_spinbox.valueChanged.connect(self.draw_by_step)

        commands_layout = QVBoxLayout()
        commands_layout.addWidget(QLabel("Step:"))
        commands_layout.addWidget(self.step_spinbox)

        main_layout = QVBoxLayout()
        main_layout.addLayout(commands_layout)
        main_layout.addWidget(self.img_label)

        self.setLayout(main_layout)

        self.draw_by_step(self.step_spinbox.value())

    def draw_by_step(self, step) -> None:
        img = QImage(600, 200, QImage.Format_RGB16)
        img.fill(Qt.white)

        painter = QPainter(img)
        painter.setPen(Qt.black)

        draw_koch(painter, 0, img.height() - 1, img.width(), img.height() - 1, step)

        self.img_label.setPixmap(QPixmap.fromImage(img))

        painter.end()


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.resize(600, 300)
    w.show()

    app.exec()
