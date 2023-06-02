#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Overlay "watermark" image / Наложение "водяного знака" на изображение

"""


# pip install Pillow
from PIL import Image, ImageDraw, ImageFont


file_name = "input.jpg"
image = Image.open(file_name)
width, height = image.size

drawer = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", 25)
text = "Hello World!"
width_text, height_text = font.getsize(text)

for i in range(0, width, width_text * 2):
    for j in range(0, height, height_text * 2):
        drawer.text((i, j), text, font=font, fill=(0x00, 0xFF, 0x00))

image.show()
