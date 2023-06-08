#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


try:
    from PyQt5.QtGui import QImage, QPainter, QColor
except:
    from PyQt4.QtGui import QImage, QPainter


image = QImage("img.jpg")
size = image.size()
width, height = size.width(), size.height()

ROW_COUNT = 3
COLUMN_COUNT = 5

grid_image = QImage(width * COLUMN_COUNT, height * ROW_COUNT, QImage.Format_RGB32)
grid_image.fill(QColor("white"))

painter = QPainter(grid_image)

for row in range(ROW_COUNT):
    y = row * width

    for column in range(COLUMN_COUNT):
        x = column * height
        painter.drawImage(x, y, image)

grid_image.save("grid_img.jpg")
