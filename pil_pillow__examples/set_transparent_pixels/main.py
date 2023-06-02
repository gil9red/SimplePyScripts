#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PIL import Image


file_name = "../for_cycle__pixels__array/input.jpg"

img = Image.open(file_name).convert("RGBA")
pixels = img.load()
width, height = img.size

for i in range(width):
    for j in range(height):
        if (j + i) % 2 == 0:
            pixels[i, j] = 0, 0, 0, 0

img.save("output.png")
