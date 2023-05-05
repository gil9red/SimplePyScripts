#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Эффект исчезновения фотографии
Кликая на области на фотографии запускаются процессы плавного увеличения
прозрачности пикселей, эффект как круги воды, будут расходиться пока не
закончатся непрозрачные пиксели
"""


import sys
import traceback


try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *

except:
    try:
        from PyQt4.QtGui import *
        from PyQt4.QtCore import *

    except:
        from PySide.QtGui import *
        from PySide.QtCore import *


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


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
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.painter.setCompositionMode(QPainter.CompositionMode_Clear)
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(Qt.transparent)

    def add(self, pos_center):
        self.circle_list.append(Timer.Circle(pos_center))

    def tick(self):
        for circle in self.circle_list:
            self.painter.drawEllipse(circle.pos_center, circle.radii, circle.radii)
            circle.next()

        self.widget.update()


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("effect_of_vanishing_photos.py")

        self.im = QImage("im.png")
        self.resize(self.im.size())

        self.timer = Timer(self, self.im)
        self.timer.start()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        self.timer.add(event.pos())

    def paintEvent(self, event):
        super().paintEvent(event)

        p = QPainter(self)
        p.setBrush(Qt.white)
        p.drawRect(self.rect())

        p.setBrush(Qt.yellow)
        p.drawRect(
            self.width() // 6, self.width() // 5, self.width() // 3, self.height() // 4
        )
        p.drawImage(0, 0, self.im)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    app.exec_()
