#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image, ImageDraw, ImageFont


image = Image.open("images.jpg")

font = ImageFont.truetype("arial.ttf", 25)
drawer = ImageDraw.Draw(image)
drawer.text((50, 100), "Hello World!\nПривет мир!", font=font, fill="black")

image.save("new_img.jpg")
image.show()
