#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import glob

# pip install pillow
from PIL import Image


for file_name in glob.glob("*.png"):
    try:
        image = Image.open(file_name)
        if not image.verify():
            raise ValueError(f"bad img {file_name}")
    except:
        print(f"{file_name} looks bad")
        try:
            os.remove(file_name)
        except:
            print(f"{file_name} looks unremovable")
