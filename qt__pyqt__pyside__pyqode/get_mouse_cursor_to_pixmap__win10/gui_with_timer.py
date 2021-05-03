#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWinExtras import QtWin

import win32gui


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.DEFAULT_MOUSE_PIXMAP = QPixmap('default_mouse.png').scaledToWidth(16)

        self.label = QLabel()

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.timer = QTimer()
        self.timer.timeout.connect(self._on_tick)
        self.timer.setInterval(100)
        self.timer.start()

    def _on_tick(self):
        # flags, hcursor, (x, y) =
        _, hcursor, _ = win32gui.GetCursorInfo()

        # fIcon, xHotspot, yHotspot, hbmMask, hbmColor =
        _, _, _, _, hbmColor = win32gui.GetIconInfo(hcursor)

        pixmap = QtWin.fromHBITMAP(hbmColor.handle, QtWin.HBitmapPremultipliedAlpha)
        if pixmap.isNull():
            pixmap = self.DEFAULT_MOUSE_PIXMAP

        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
