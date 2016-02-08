#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# http://www.blog.pythonlibrary.org/2014/10/22/pywin32-how-to-set-desktop-background/


# # based on http://dzone.com/snippets/set-windows-desktop-wallpaper
# import win32api, win32con, win32gui
#
# #----------------------------------------------------------------------
# def setWallpaper(path):
#     key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
#     win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
#     win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
#     win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1+2)
#
# if __name__ == "__main__":
#     path = r'C:\Users\Public\Pictures\Sample Pictures\Jellyfish.jpg'
#     setWallpaper(path)


# import ctypes
# import win32con
#
# def setWallpaperWithCtypes(path):
#     # This code is based on the following two links
#     # http://mail.python.org/pipermail/python-win32/2005-January/002893.html
#     # http://code.activestate.com/recipes/435877-change-the-wallpaper-under-windows/
#     cs = ctypes.c_buffer(path)
#     ok = ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_SETDESKWALLPAPER, 0, cs, 0)
#
# if __name__ == "__main__":
#     path = r'C:\Users\Public\Pictures\Sample Pictures\Jellyfish.jpg'
#     setWallpaperWithCtypes(path)
