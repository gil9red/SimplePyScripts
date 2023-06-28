#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes
from ctypes.wintypes import RECT


FindWindow = ctypes.windll.user32.FindWindowW

# BOOL WINAPI GetWindowRect(
#   _In_  HWND   hWnd,
#   _Out_ LPRECT lpRect
# );
GetWindowRect = ctypes.windll.user32.GetWindowRect


hwnd = FindWindow("Shell_TrayWnd", None)
print(hwnd)

rect = RECT()
ok = GetWindowRect(hwnd, ctypes.pointer(rect))
print(ok)

print(rect.left, rect.top, rect.right, rect.bottom)
