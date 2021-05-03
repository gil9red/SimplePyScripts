#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication
from PyQt5.QtWinExtras import QtWin

import win32gui


app = QApplication([])

# flags, hcursor, (x, y) =
_, hcursor, _ = win32gui.GetCursorInfo()

# fIcon, xHotspot, yHotspot, hbmMask, hbmColor =
_, _, _, _, hbmColor = win32gui.GetIconInfo(hcursor)

pixmap = QtWin.fromHBITMAP(hbmColor.handle, QtWin.HBitmapPremultipliedAlpha)
print(pixmap.size(), pixmap)

pixmap.save('img.png')
