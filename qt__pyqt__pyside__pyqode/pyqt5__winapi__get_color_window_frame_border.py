#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes
from PyQt5 import Qt


COLOR_ACTIVEBORDER = 10

GetSysColorBrush = ctypes.windll.user32.GetSysColorBrush
GetSysColor = ctypes.windll.user32.GetSysColor


def GetRValue(value):
    return value & 0xFF


def GetGValue(value):
    return value >> 8 & 0xFF


def GetBValue(value):
    return value >> 16 & 0xFF


def getWindowFrameColor():
    # This is the only way to detect that a given color is supported
    brush = GetSysColorBrush(COLOR_ACTIVEBORDER)
    if brush:
        color = GetSysColor(COLOR_ACTIVEBORDER)
        return Qt.QColor(GetRValue(color), GetGValue(color), GetBValue(color))

    return Qt.QColor()


if __name__ == "__main__":
    app = Qt.QApplication([])

    def get_color() -> None:
        color = getWindowFrameColor()
        button.setStyleSheet("background-color: " + color.name())

    button = Qt.QPushButton("Get")
    button.clicked.connect(get_color)
    button.resize(100, 100)
    button.show()

    app.exec()
