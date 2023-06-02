#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image


image_file = "Collapse all.png"
img = Image.open(image_file).convert("RGBA")

pixdata = img.load()

# Делаем темнее картинку, игнорируя фон
for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pixdata[x, y][:3] != (255, 255, 255):
            pixdata[x, y] = (
                tuple(map(lambda x: x - 50, pixdata[x, y][:3])) + pixdata[x, y][3:]
            )

img.save("Collapse all black.png")
