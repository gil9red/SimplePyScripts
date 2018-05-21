#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


with open('input.jpg', 'rb') as f:
    data = f.read()

import io
data_io = io.BytesIO(data)

# pip install Pillow
from PIL import Image
img = Image.open(data_io)
print(img)

img.show()
