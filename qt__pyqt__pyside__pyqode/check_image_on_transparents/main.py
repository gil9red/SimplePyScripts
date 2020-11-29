#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QRect


FILE_NAME = 'emoji-video-game-512x512.png'


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.img = QPixmap()
        self.img.load(FILE_NAME)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setBrush(Qt.darkGreen)
        painter.drawRect(self.rect())

        img_rect = self.img.rect()
        dev_rect = QRect(0, 0, painter.device().width(), painter.device().height())
        img_rect.moveCenter(dev_rect.center())

        painter.drawPixmap(img_rect.topLeft(), self.img)


if __name__ == '__main__':
    app = QApplication([])

    mw = Widget()
    mw.show()

    app.exec()
