#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Fullscreen


import datetime as DT

# pip install pyscreenshot
import pyscreenshot as ImageGrab


PATTERN = 'pyscreenshot__screenshot'


img = ImageGrab.grab()
img.save(f'{PATTERN}.png')
img.save(f'{PATTERN}.jpg')
# img.show()

# Filename with datetime
file_name = f'{PATTERN}_{DT.datetime.now():%Y-%m-%d_%H%M%S}.jpg'
print(file_name)

img.save(file_name)
