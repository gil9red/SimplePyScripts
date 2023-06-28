#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# TODO: почему-то не работает

import win32gui
import win32api
import win32con


hwnd = win32gui.FindWindow("TAIMPTrayControl", None)
print(hwnd)

# hwnd = win32gui.FindWindow('TApplication', '')
# print(hwnd)

hwnd = win32gui.FindWindow("TAIMPMainForm", None)
print(hwnd)

key = win32con.VK_F2
lparam1 = win32api.MapVirtualKey(key, 0) << 16 | 1
lparam2 = 1 << 31 | 1 << 30 | win32api.MapVirtualKey(key, 0) << 16 | 1

pl1_key = win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, lparam1)
pl2_key = win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, lparam2)
print(pl1_key, pl2_key)


# print(win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F2))
# print(win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F2))

# print(win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F2, 0))
# print(win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F2, 0))

# def foo():a=win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F2); b=win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F2, 0);return a,b
