#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


file_name = "input.png"
new_file_name = file_name[:-3] + 'jpg'

from PIL import Image
img = Image.open(file_name)

img.save(new_file_name, optimize=True, quality=100)
