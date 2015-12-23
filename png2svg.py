#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os.path
import sys

from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtSvg import *


# TODO: load svg, transform svg and save as svg


if __name__ == '__main__':
    app = QApplication(sys.argv)

    file_name = r'C:\Users\ipetrash\Desktop\Move_left.png'

    im = QImage()
    im.load(file_name)
    w, h = im.size().width(), im.size().height()

    gen = QSvgGenerator()
    gen.setFileName(os.path.splitext(file_name)[0] + '.svg')
    gen.setSize(im.size())
    gen.setViewBox(QRect(0, 0, w, h))

    painter = QPainter()
    painter.begin(gen)
    painter.drawImage(QPointF(0, 0),
                      im,
                      QRectF(0, 0, w, h))
    painter.end()
