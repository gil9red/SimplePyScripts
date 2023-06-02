#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import ImageQt

# pip install pyqt5
from PyQt5.Qt import QImage, QPixmap, QApplication


image_file = "input.jpg"

app = QApplication([])

img_image = QImage(image_file)
pix_image = QPixmap(image_file)

pil_img_image = ImageQt.fromqimage(img_image)
pil_img_image.show()

pil_pix_image = ImageQt.fromqimage(pix_image)
pil_pix_image.show()
