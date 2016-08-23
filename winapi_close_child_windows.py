#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт ищет у запущенного Notepad++ панели инструментов и закрывает их."""


from win32gui import *
from win32con import *


def all_ok(hwnd, param):
    text = GetWindowText(hwnd)
    class_name = GetClassName(hwnd)
    print('#{:0>8x} "{}": {}'.format(hwnd, text, class_name))

    # Закрытие панели инструментов
    if class_name == 'ToolbarWindow32':
        PostMessage(hwnd, WM_CLOSE, 0, 0)

    return True

hwnd = FindWindow('Notepad++', None)
EnumChildWindows(hwnd, all_ok, None)
