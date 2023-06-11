#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


# Colors from: https://github.com/gabrielecirulli/2048/blob/master/style/main.css#L324
COLORS_OF_2048 = [
    ("#3c3a32", 4096),
    ("#edc22e", 2048),
    ("#edc53f", 1024),
    ("#edc850", 512),
    ("#edcc61", 256),
    ("#edcf72", 128),
    ("#f65e3b", 64),
    ("#f67c5f", 32),
    ("#f59563", 16),
    ("#f2b179", 8),
    ("#ede0c8", 4),
    ("#eee4da", 2),
    ("#eee4da", 0),
]

app = QApplication([])

w = QWidget()

layout = QGridLayout()
w.setLayout(layout)
w.show()

row = 0
for color_hex, number in COLORS_OF_2048:
    pix = QPixmap(40, 40)
    pix.fill(QColor(color_hex))  # 4096

    label_pix = QLabel()
    label_pix.setPixmap(pix)

    layout.addWidget(QLabel(str(number)), row, 0)
    layout.addWidget(label_pix, row, 1)

    row += 1


app.exec()
