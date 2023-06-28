#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт для получения правильного значения раскладки клавиатуры в Windows для консольных
процессов.

Хитрость в том, что для консольных процессов всегда возвращается одно и тоже значение раскладки.

"""


# Переписал на python используя этот ответ: http://stackoverflow.com/a/12383335/5909792


from ctypes import *


user32 = windll.user32
kernel32 = windll.kernel32


class RECT(Structure):
    _fields_ = [
        ("left", c_ulong),
        ("top", c_ulong),
        ("right", c_ulong),
        ("bottom", c_ulong),
    ]


class GUITHREADINFO(Structure):
    _fields_ = [
        ("cbSize", c_ulong),
        ("flags", c_ulong),
        ("hwndActive", c_ulong),
        ("hwndFocus", c_ulong),
        ("hwndCapture", c_ulong),
        ("hwndMenuOwner", c_ulong),
        ("hwndMoveSize", c_ulong),
        ("hwndCaret", c_ulong),
        ("rcCaret", RECT),
    ]


if __name__ == "__main__":
    gti = GUITHREADINFO(cbSize=sizeof(GUITHREADINFO))
    user32.GetGUIThreadInfo(0, byref(gti))

    dwThread = user32.GetWindowThreadProcessId(gti.hwndActive, 0)
    lang = user32.GetKeyboardLayout(dwThread)
    print(hex(lang))
