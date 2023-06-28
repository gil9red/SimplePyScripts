#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import win32gui
import win32api
import win32con


h = win32gui.FindWindow(None, "Untitled - Notepad")
print(h)

if h:
    child = win32gui.FindWindowEx(h, None, "Edit", None)
    pl = win32api.SendMessage(child, win32con.WM_CHAR, ord("D"), 1)

    # OR:

    lparam1 = win32api.MapVirtualKey(win32con.VK_F5, 0) << 16 | 1
    lparam2 = 1 << 31 | 1 << 30 | win32api.MapVirtualKey(win32con.VK_F5, 0) << 16 | 1

    # pl1_F5 = win32api.PostMessage(child, win32con.WM_KEYDOWN, win32con.VK_F5, lparam1)
    # pl2_F5 = win32api.PostMessage(child, win32con.WM_KEYUP, win32con.VK_F5, lparam2)

    pl1_F5 = win32api.PostMessage(child, win32con.WM_KEYDOWN, ord("D"), lparam1)
    pl2_F5 = win32api.PostMessage(child, win32con.WM_KEYUP, ord("D"), lparam2)
