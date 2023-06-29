#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Fullscreen


import datetime as dt

# pip install pyscreenshot
import pyscreenshot as ImageGrab

from config import DIR_OUTPUT


PATTERN = DIR_OUTPUT / f"pyscreenshot__screenshot"


img = ImageGrab.grab()
img.save(f"{PATTERN}.png")
img.save(f"{PATTERN}.jpg")
# img.show()

# Filename with datetime
file_name = f"{PATTERN}_{dt.datetime.now():%Y-%m-%d_%H%M%S}.jpg"
print(file_name)

img.save(file_name)
