#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes
import tkinter


def get_screen_info() -> tuple[int, int, int]:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    root = tkinter.Tk()

    width = ctypes.windll.user32.GetSystemMetrics(0)
    height = ctypes.windll.user32.GetSystemMetrics(1)

    dpi = ctypes.windll.user32.GetDpiForWindow(root.winfo_id())

    # Destroy the window
    root.destroy()

    return width, height, dpi


if __name__ == "__main__":
    width, height, dpi = get_screen_info()
    print(width, height, dpi)
