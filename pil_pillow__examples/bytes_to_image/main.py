#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import io

# pip install Pillow
from PIL import Image


with open("input.jpg", "rb") as f:
    data = f.read()

data_io = io.BytesIO(data)
img = Image.open(data_io)
print(img)

img.show()
