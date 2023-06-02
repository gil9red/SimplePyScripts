#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image


image_file = "input.jpg"
img = Image.open(image_file)

size = 128, 128

img.thumbnail(size)
img.save("output_thumbnail.png")
img.show()
