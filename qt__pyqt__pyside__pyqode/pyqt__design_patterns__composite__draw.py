#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Composite - Компоновщик
# SOURCE: https://ru.wikipedia.org/wiki/Компоновщик_(шаблон_проектирования)


import sys
import traceback

from abc import ABCMeta, abstractmethod

from PyQt5.Qt import *


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "{}: {}:\n".format(ex_cls.__name__, ex)
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class Graphic(metaclass=ABCMeta):
    @abstractmethod
    def draw(self, painter: QPainter):
        pass


class CompositeGraphic(Graphic):
    def __init__(self):
        self.__child_graphics: list[Graphic] = []

    def draw(self, painter: QPainter):
        for graphic in self.__child_graphics:
            graphic.draw(painter)

    # Adds the graphic to the composition
    def add(self, graphic: Graphic):
        if graphic in self.__child_graphics:
            return

        self.__child_graphics.append(graphic)

    # Removes the graphic from the composition
    def remove(self, graphic: Graphic):
        self.__child_graphics.remove(graphic)


class Ellipse(Graphic):
    def __init__(self, x, y, rx, ry):
        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry

    def draw(self, painter: QPainter):
        painter.drawEllipse(self.x, self.y, self.rx, self.ry)


class Point(Graphic):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, painter: QPainter):
        painter.drawPoint(self.x, self.y)


class Rect(Graphic):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, painter: QPainter):
        painter.drawRect(self.x, self.y, self.w, self.h)


class Line(Graphic):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

    def draw(self, painter: QPainter):
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)


class CanvasWidget(QWidget):
    def __init__(self, graphic: Graphic):
        super().__init__()

        self.setWindowTitle("Canvas")

        self.graphic = graphic

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(Qt.green)

        self.graphic.draw(painter)


if __name__ == "__main__":
    ellipse_1 = Ellipse(x=50, y=50, rx=10, ry=15)
    ellipse_2 = Ellipse(x=10, y=5, rx=40, ry=50)

    composite_1 = CompositeGraphic()
    composite_1.add(ellipse_1)
    composite_1.add(Point(4, 4))
    composite_1.add(Point(4, 5))
    composite_1.add(Point(4, 6))

    composite_main = CompositeGraphic()
    composite_main.add(ellipse_2)
    composite_main.add(Rect(30, 20, 50, 30))
    composite_main.add(Rect(100, 70, 50, 50))
    composite_main.add(composite_1)
    composite_main.add(Line(60, 10, 25, 25))

    # Run
    app = QApplication([])

    mw = CanvasWidget(composite_main)
    mw.show()

    app.exec()
