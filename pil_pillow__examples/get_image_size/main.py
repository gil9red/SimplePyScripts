#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image


img = Image.open("input.jpg")
print(img)
print(img.size)
# img.show()
