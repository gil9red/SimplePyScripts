#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image

from PyQt5 import Qt


image_file = "input.jpg"
image = Image.open(image_file)

app = Qt.QApplication([])

label_image = Qt.QLabel()
pix_1 = Qt.QPixmap.fromImage(image.toqimage().copy())
label_image.setPixmap(pix_1)

label_pixmap = Qt.QLabel()
pix_2 = image.toqpixmap()
label_pixmap.setPixmap(pix_2)

layout = Qt.QHBoxLayout()
layout.addWidget(label_image)
layout.addWidget(label_pixmap)

w = Qt.QWidget()
w.setLayout(layout)
w.show()

app.exec()
