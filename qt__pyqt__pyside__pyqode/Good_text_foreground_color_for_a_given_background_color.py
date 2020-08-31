#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


# SOURCE: https://stackoverflow.com/a/3943023/5909792
def get_good_text_foreground_color(color: QColor) -> QColor:
    _, r, g, b = color.getRgb()

    if (r * 0.299 + g * 0.587 + b * 0.114) > 186:
        return QColor(Qt.black)

    return QColor(Qt.white)
