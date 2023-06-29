#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Fullscreen


import datetime as dt
from PyQt5.QtWidgets import QApplication
from config import DIR_OUTPUT


PATTERN = DIR_OUTPUT / f"PyQt5__screenshot"


app = QApplication([])


img = app.primaryScreen().grabWindow(QApplication.desktop().winId())
img.save(f"{PATTERN}.png")
img.save(f"{PATTERN}.jpg")

# Filename with datetime
file_name = f"{PATTERN}_{dt.datetime.now():%Y-%m-%d_%H%M%S}.jpg"
print(file_name)

img.save(file_name)
