#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject


class Signals(QObject):
    about_image = pyqtSignal(str, QImage)


class ThumbnailWorker(QRunnable):
    def __init__(self, file_name: str, width, height):
        super().__init__()

        self.file_name = file_name
        self.width = width
        self.height = height
        self.signals = Signals()

    def run(self):
        img = QImage(self.file_name)
        if img.isNull():
            return

        img = img.scaled(self.width, self.height)
        self.signals.about_image.emit(self.file_name, img)
