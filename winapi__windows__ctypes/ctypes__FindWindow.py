#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes


FindWindow = ctypes.windll.user32.FindWindowW


hwnd = FindWindow("Shell_TrayWnd", None)
print(hwnd)
