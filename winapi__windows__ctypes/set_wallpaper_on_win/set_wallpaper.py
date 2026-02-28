#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# http://www.blog.pythonlibrary.org/2014/10/22/pywin32-how-to-set-desktop-background/


# based on http://dzone.com/snippets/set-windows-desktop-wallpaper
import win32api
import win32con
import win32gui


def set_wallpaper(file_name) -> None:
    key = win32api.RegOpenKeyEx(
        win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE
    )
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, file_name, 1 + 2)


if __name__ == "__main__":
    file_name = r"C:\Users\Public\Pictures\Sample Pictures\Jellyfish.jpg"
    set_wallpaper(file_name)
