#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


app = QApplication([])

w = QWidget()

pix = QPixmap("img.png")

layout = QGridLayout()
w.setLayout(layout)
w.show()

row = 0
for width, height in [(24, 24), (32, 32), (48, 48), (96, 96), (128, 128), (256, 256)]:
    label_pix = QLabel()
    label_pix.setPixmap(pix.scaled(QSize(width, height)))

    layout.addWidget(QLabel("{}x{}".format(width, height)), row, 0)
    layout.addWidget(label_pix, row, 1)

    row += 1

app.exec()
