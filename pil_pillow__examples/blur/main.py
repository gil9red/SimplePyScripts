#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image, ImageFilter


image_file = "input.jpg"
img = Image.open(image_file)

img = img.filter(ImageFilter.GaussianBlur(2))
img.save("output.png")
img.show()
