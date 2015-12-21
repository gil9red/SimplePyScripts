#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: почему-то не работает

import win32gui

hwnd = win32gui.FindWindow('tAIMPTrayControl', None)
print(hwnd)

import win32api
import win32con

print(win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F2))
print(win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F2))

# def foo():a=win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F2); b=win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F2, 0);return a,b