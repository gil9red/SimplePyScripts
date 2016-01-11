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
        class Circle:
            def __init__(self, pos_center):
                self.pos_center = pos_center
                self.radii = 1

            def next(self):
                self.radii += 1

        def __init__(self, widget, image):
            super().__init__()

            self.circle_list = list()

            self.widget = widget

            self.setInterval(60)
            self.timeout.connect(self.tick)

            self.painter = QPainter(image)
            self.painter.setCompositionMode(QPainter.CompositionMode_SourceOut)
            self.painter.setPen(Qt.NoPen)
            self.painter.setBrush(Qt.transparent)

        def add(self, pos_center):
            self.circle_list.append(Widget.Timer.Circle(pos_center))

        def tick(self):
            for circle in self.circle_list:
                self.painter.drawEllipse(circle.pos_center, circle.radii, circle.radii)
                circle.next()

            self.widget.update()

    def __init__(self):
        super().__init__()

        self.resize(200, 200)

        self.im = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self.im.fill(Qt.black)

        self.timer = Widget.Timer(self, self.im)
        self.timer.start()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        self.timer.add(event.posF())

    def paintEvent(self, event):
        super().paintEvent(event)

        p = QPainter(self)
        p.setBrush(Qt.yellow)
        p.drawRect(40, 40, 80, 80)

        p.drawImage(0, 0, self.im)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    app.exec_()
