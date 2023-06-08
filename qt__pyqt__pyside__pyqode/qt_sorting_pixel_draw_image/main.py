#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys
import random
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import QTimer


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


DIR = Path(__file__).resolve().parent
IMG_FILE_NAME = str(DIR / "img.png")


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(DIR.name)

        self.img = QImage(IMG_FILE_NAME)
        width = self.img.size().width()
        height = self.img.size().height()
        self.img = self.img.scaled(width * 3, height * 3)
        self.img_width = self.img.size().width()
        self.img_height = self.img.size().height()

        # Размер окна под размер картинок
        self.resize(self.img_width * 2 + 20, self.img_height + 20)

        # Сгенерируем список координат пикселей
        self.pixel_matrix = []
        for y in range(self.img_height):
            row = [(y, x) for x in range(self.img_width)]
            random.shuffle(row)
            self.pixel_matrix.append(row)

        random.shuffle(self.pixel_matrix)

        self.new_img = QImage(self.img_width, self.img_height, QImage.Format_RGB32)
        for y, row in enumerate(self.pixel_matrix):
            for x, (y2, x2) in enumerate(row):
                pixel = self.img.pixel(x2, y2)  # Берем пиксели из другой позиции
                self.new_img.setPixel(x, y, pixel)

        self.timer = QTimer()
        self.timer.timeout.connect(self._draw_pixel)
        self.timer.start(15)  # ms

    def _draw_pixel(self):
        if not self.pixel_matrix:
            self.timer.stop()
            return

        row = self.pixel_matrix.pop()
        row.sort()

        for y, x in row:
            pixel = self.img.pixel(x, y)
            self.new_img.setPixel(x, y, pixel)

        # Перерисование виджета
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Рисуем старую картинку
        painter.drawImage(0, 0, self.img)

        # Рисуем новую картинку
        painter.drawImage(0 + self.img.width() + 10, 0, self.new_img)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    # w.resize(200, 100)
    w.show()

    app.exec()
