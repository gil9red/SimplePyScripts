#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
import sys

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QPainter, QImage
    from PyQt5.QtCore import QPointF, QRectF, QRect
    from PyQt5.QtSvg import QSvgGenerator

except:
    try:
        from PyQt4.QtGui import QApplication, QPainter, QImage
        from PyQt4.QtCore import QPointF, QRectF, QRect
        from PyQt4.QtSvg import QSvgGenerator

    except:
        from PySide.QtGui import QApplication, QPainter, QImage
        from PySide.QtCore import QPointF, QRectF, QRect
        from PySide.QtSvg import QSvgGenerator


if __name__ == "__main__":
    app = QApplication(sys.argv)

    file_name = r"C:\Users\ipetrash\Desktop\explorer.png"

    im = QImage()
    im.load(file_name)
    w, h = im.size().width(), im.size().height()

    gen = QSvgGenerator()
    gen.setFileName(os.path.splitext(file_name)[0] + ".svg")
    gen.setSize(im.size())
    gen.setViewBox(QRect(0, 0, w, h))

    painter = QPainter()
    painter.begin(gen)
    painter.drawImage(QPointF(0, 0), im, QRectF(0, 0, w, h))
    painter.end()
