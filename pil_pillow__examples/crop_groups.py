#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

# pip install Pillow
from PIL import Image


path = Path(...)

for file_name in path.glob("*.jpg"):
    img = Image.open(file_name)
    width, height = img.size

    x1, y1, x2, y2 = 393, 0, width, height
    cropped_img = img.crop((x1, y1, x2, y2))
    cropped_img.save(file_name)

    # cropped_img.show()
    # break
