#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PIL import Image


img = Image.open("input.jpg")
img.save("output.jpg", format="JPEG", quality=1)
