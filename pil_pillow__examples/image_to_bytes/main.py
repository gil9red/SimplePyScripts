#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import io

# pip install Pillow
from PIL import Image


img = Image.open("input.jpg")

bytes_io = io.BytesIO()
img.save(bytes_io, img.format)

img_data = bytes_io.getvalue()
print(len(img_data), img_data)

# NOTE: For read() need call seek
bytes_io.seek(0)
print(bytes_io.read(10))
