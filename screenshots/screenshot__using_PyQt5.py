#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Fullscreen


import datetime as DT

from PyQt5.QtWidgets import QApplication


PATTERN = 'PyQt5__screenshot'


app = QApplication([])


img = app.primaryScreen().grabWindow(QApplication.desktop().winId())
img.save(PATTERN + '.png')
img.save(PATTERN + '.jpg')

# Filename with datetime
file_name = f'{PATTERN}_{DT.datetime.now():%Y-%m-%d_%H%M%S}.jpg'
print(file_name)

img.save(file_name)
