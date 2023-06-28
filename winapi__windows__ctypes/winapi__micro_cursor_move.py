#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Для того, чтобы винда не разлогинивалась от бездействия."""


import time
import win32api


delay = 60

try:
    while True:
        x, y = win32api.GetCursorPos()

        win32api.SetCursorPos((x + 1, y))
        win32api.SetCursorPos((x - 1, y))

        time.sleep(delay)

except KeyboardInterrupt:
    pass
