#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PIL import Image, ImageDraw


img = Image.open("input.jpg")
bigsize = img.size[0] * 3, img.size[1] * 3
mask = Image.new("L", bigsize, 0)

draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0) + bigsize, fill=255)

mask = mask.resize(img.size, Image.ANTIALIAS)
img.putalpha(mask)
img.save("output.png")
