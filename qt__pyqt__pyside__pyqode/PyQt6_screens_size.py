#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication


app = QApplication([])
for screen in QApplication.screens():
    print(screen.geometry(), screen.size())
"""
PyQt6.QtCore.QRect(0, 0, 1920, 1080) PyQt6.QtCore.QSize(1920, 1080)
PyQt6.QtCore.QRect(-3840, 0, 1536, 864) PyQt6.QtCore.QSize(1536, 864)
PyQt6.QtCore.QRect(-1920, 0, 1920, 1080) PyQt6.QtCore.QSize(1920, 1080)
"""

app = None
print()

app = QGuiApplication([])
for screen in QGuiApplication.screens():
    print(screen.geometry(), screen.size())
"""
PyQt6.QtCore.QRect(0, 0, 1920, 1080) PyQt6.QtCore.QSize(1920, 1080)
PyQt6.QtCore.QRect(-3840, 0, 1536, 864) PyQt6.QtCore.QSize(1536, 864)
PyQt6.QtCore.QRect(-1920, 0, 1920, 1080) PyQt6.QtCore.QSize(1920, 1080)
"""
