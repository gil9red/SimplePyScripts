#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import win32gui

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWinExtras import QtWin


app = QApplication([])

# flags, hcursor, (x, y) =
_, hcursor, _ = win32gui.GetCursorInfo()

# fIcon, xHotspot, yHotspot, hbmMask, hbmColor =
_, _, _, _, hbmColor = win32gui.GetIconInfo(hcursor)

pixmap = QtWin.fromHBITMAP(hbmColor.handle, QtWin.HBitmapPremultipliedAlpha)
print(pixmap.size(), pixmap)

pixmap.save("img.png")
