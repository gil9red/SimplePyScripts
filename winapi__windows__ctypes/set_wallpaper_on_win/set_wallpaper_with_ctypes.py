#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# http://www.blog.pythonlibrary.org/2014/10/22/pywin32-how-to-set-desktop-background/


import ctypes


SPI_SETDESKWALLPAPER = 20


def set_wallpaper_with_ctypes(file_name) -> None:
    # This code is based on the following two links
    # http://mail.python.org/pipermail/python-win32/2005-January/002893.html
    # http://code.activestate.com/recipes/435877-change-the-wallpaper-under-windows/
    cs = ctypes.c_buffer(file_name)
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, cs, 0)


if __name__ == "__main__":
    file_name = r"C:\Users\Public\Pictures\Sample Pictures\Jellyfish.jpg"
    set_wallpaper_with_ctypes(file_name)
