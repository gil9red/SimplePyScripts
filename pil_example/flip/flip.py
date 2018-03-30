#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PIL import Image, ImageOps
img = Image.open('img.png')
img = ImageOps.flip(img)
img.show()
