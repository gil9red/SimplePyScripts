#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback
import random

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import Qt, QTimer


def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


IMG_FILE_NAME = "img.png"


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("qt_pixel_draw_image")

        self.img = QImage(IMG_FILE_NAME)
        self.img_width = self.img.size().width()
        self.img_height = self.img.size().height()

        # Сгенерируем список координат пикселей
        self.pixel_list = [
            (y, x) for y in range(self.img_height) for x in range(self.img_width)
        ]
        # OR:
        # self.pixel_list = []
        # for y in range(self.img_height):
        #     for x in range(self.img_width):
        #         self.pixel_list.append((y, x))

        # Перемешаем элементы списка случайным образом
        random.shuffle(self.pixel_list)

        self.new_img = QImage(self.img_width, self.img_height, QImage.Format_RGB32)
        self.new_img.fill(Qt.white)

        self.timer = QTimer()
        self.timer.timeout.connect(self._draw_pixel)
        self.timer.start(1)  # 1 ms

    def _draw_pixel(self) -> None:
        # Если список пустой
        if not self.pixel_list:
            self.timer.stop()
            return

        y, x = self.pixel_list.pop()
        pixel = self.img.pixel(x, y)

        # Установка пикселя в новой картинке
        self.new_img.setPixel(x, y, pixel)

        # Перерисование виджета
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        # Рисуем старую картинку
        painter.drawImage(0, 0, self.img)

        # Рисуем новую картинку
        painter.drawImage(0 + self.img.width() + 10, 0, self.new_img)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.resize(200, 100)
    w.show()

    app.exec()
