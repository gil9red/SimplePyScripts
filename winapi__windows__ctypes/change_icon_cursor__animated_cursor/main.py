#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import ctypes

import win32gui
import win32con


# SOURCE: https://stackoverflow.com/a/55979357/5909792

# SOURCE: http://www.rw-designer.com/cursor-detail/106595
FILE_NAME_CURSOR = "fidget spinner animated normal select.ani"

hold = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
hsave = ctypes.windll.user32.CopyImage(
    hold, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE
)

hnew = win32gui.LoadImage(
    0, FILE_NAME_CURSOR, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE
)
ctypes.windll.user32.SetSystemCursor(hnew, 32512)
time.sleep(10)

# Restore the old cursor
ctypes.windll.user32.SetSystemCursor(hsave, 32512)
