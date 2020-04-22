#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Fullscreen


import datetime as DT

# pip install pillow
from PIL import ImageGrab


im = ImageGrab.grab()
im.save('screenshot.png')
im.save('screenshot.jpg')
im.show()

# Filename with datetime
file_name = f'screenshot_{DT.datetime.now():%Y-%m-%d_%H%M%S}.jpg'
print(file_name)

im.save(file_name)
