#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import itertools

# pip install Pillow
from PIL import Image, ImageDraw, ImageFont


img = Image.new('RGB', (500, 300), (255, 0, 0))
width, height = img.size

drawer = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 25)

text_0, text_1 = "0", "1"
color_0, color_1 = (0, 0, 0), (255, 255, 255)
it = itertools.cycle([
    (text_0, color_0), (text_1, color_1)
])

width_text_0, height_text_0 = font.getsize(text_0)
width_text_1, height_text_1 = font.getsize(text_1)

max_width_text = max(width_text_0, width_text_1)
max_height_text = max(height_text_0, height_text_1)

for i in range(0, width // max_width_text):
    for j in range(0, height // max_height_text):
        x, y = i * max_width_text, j * max_height_text
        text, color = next(it)

        drawer.text((x, y), text, font=font, fill=color)

    # NOTE: aligned column
    # next(it)

img.save("output.png")
img.show()
