#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
The script looks for in a running Notepad ++ toolbar and closes them.

Скрипт ищет у запущенного Notepad++ панели инструментов и закрывает их.
"""


import win32gui
import win32con


def all_ok(hwnd, param):
    text = win32gui.GetWindowText(hwnd)
    class_name = win32gui.GetClassName(hwnd)
    print(f'#{hwnd:0>8x} "{text}": {class_name}')

    # Закрытие панели инструментов
    if class_name == 'ToolbarWindow32':
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    return True


def close_toolbars():
    hwnd = win32gui.FindWindow('Notepad++', None)
    if not hwnd:
        print('Window "Notepad++" not found!')
        return

    win32gui.EnumChildWindows(hwnd, all_ok, None)


if __name__ == '__main__':
    close_toolbars()
