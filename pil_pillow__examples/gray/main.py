#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image, ImageOps


image_file = "input.jpg"
image = Image.open(image_file)

image_gray = ImageOps.grayscale(image)
image_gray.save("image_gray.png")
image_gray.show()
