#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Эффект исчезновения фотографии
Кликая на области на фотографии запускаются процессы плавного увеличения
прозрачности пикселей, эффект как круги воды, будут расходиться пока не
закончатся непрозрачные пиксели"""


import sys

from PySide.QtGui import *
from PySide.QtCore import *


class Widget(QWidget):
    class Timer(QTimer):
        def __init__(self, widget, pos_center, image):
            super().__init__()

            self.pos_center = pos_center
            self.radii = 1
            self.im = image
            self.widget = widget

            self.setInterval(333)
            self.timeout.connect(self.tick)

        def tick(self):
            p = QPainter(self.im)
            p.setCompositionMode(QPainter.CompositionMode_DestinationOut)
            p.setBrush(Qt.white)
            p.drawEllipse(self.pos_center, self.radii, self.radii)

            self.radii += 1

            self.widget.update()

        def run(self):
            self.start()
            return self

    def __init__(self):
        super().__init__()

        self.resize(200, 200)

        self.im = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self.im.fill(Qt.black)

        self.timers = list()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        self.timers.append(
            Widget.Timer(self, event.posF(), self.im).run()
        )

    def paintEvent(self, event):
        super().paintEvent(event)

        p = QPainter(self)
        p.drawImage(0, 0, self.im)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    app.exec_()
