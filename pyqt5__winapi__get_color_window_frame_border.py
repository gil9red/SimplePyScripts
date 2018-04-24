#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5 import Qt

COLOR_ACTIVEBORDER = 10

import ctypes
GetSysColorBrush = ctypes.windll.user32.GetSysColorBrush
GetSysColor = ctypes.windll.user32.GetSysColor


def GetRValue(value):
    return value & 0xff


def GetGValue(value):
    return value >> 8 & 0xff


def GetBValue(value):
    return value >> 16 & 0xff


def getWindowFrameColor():
    # This is the only way to detect that a given color is supported
    brush = GetSysColorBrush(COLOR_ACTIVEBORDER)
    if brush:
        color = GetSysColor(COLOR_ACTIVEBORDER)
        return Qt.QColor(GetRValue(color), GetGValue(color), GetBValue(color))

    return Qt.QColor()


if __name__ == '__main__':
    app = Qt.QApplication([])

    def get_color():
        color = getWindowFrameColor()
        button.setStyleSheet('background-color: ' + color.name())

    button = Qt.QPushButton('Get')
    button.clicked.connect(get_color)
    button.resize(100, 100)
    button.show()

    app.exec()
