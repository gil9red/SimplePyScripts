#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image, ImageOps


img = Image.open("input.png")
img = ImageOps.flip(img)
img.show()
