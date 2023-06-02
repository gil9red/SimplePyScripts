#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image


image_file = "blur/input.jpg"
img = Image.open(image_file)

cropped_img = img.crop((175, 42, 336, 170))
cropped_img.show()
