#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import glob
import os

from PIL import Image


SIZE_THUMBS = 75, 75
FROM_DIR = "images"
TO_DIR = "thumbs"


if not os.path.exists(TO_DIR):
    os.mkdir(TO_DIR)

for filename in glob.glob(FROM_DIR + "/*.jpg"):
    filename_thumbnail = os.path.join(TO_DIR, os.path.split(filename)[1])
    print(f"{filename} -> {filename_thumbnail}")

    im = Image.open(filename)
    im.thumbnail(SIZE_THUMBS)
    im.save(filename_thumbnail)
