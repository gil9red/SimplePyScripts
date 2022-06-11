#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install Pillow
from PIL import Image


image_file = "input.png"
img = Image.open(image_file).convert('RGBA')

pixdata = img.load()

for y in range(img.size[1]):
    for x in range(img.size[0]):
        alpha = pixdata[x, y][3]
        if alpha:
            pixdata[x, y] = (255, 255, 255, alpha)

img.save("output.png")
