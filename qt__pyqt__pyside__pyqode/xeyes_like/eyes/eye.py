#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, field

from PyQt5.QtGui import QBrush, QPen, QPainter
from PyQt5.QtCore import QPoint, Qt

from .common import (
    Ellipse,
    Line,
    ResultCrossLineAndEllipse,
    is_ellipse_and_direct,
    percent_number,
)


@dataclass
class EllipseObject:
    center: QPoint = field(default_factory=lambda: QPoint(0, 0))
    radiusX: float = 0.0
    radiusY: float = 0.0

    brush: QBrush = Qt.black
    pen: QPen = field(default_factory=lambda: QPen(Qt.black, 1.0))


@dataclass
class Iris(EllipseObject):
    """Радужка"""


@dataclass
class Pupil(EllipseObject):
    """Зрачок"""


@dataclass
class Eye(EllipseObject):
    """Глаз"""

    iris: Iris = field(default_factory=Iris)
    pupil: Pupil = field(default_factory=Pupil)

    visible_iris: bool = True
    visible_pupil: bool = True

    def draw(self, painter: QPainter):
        self.draw_eye(painter)
        self.draw_iris(painter)
        self.draw_pupil(painter)

    def draw_eye(self, painter: QPainter):
        painter.save()
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawEllipse(self.center, self.radiusX, self.radiusY)
        painter.restore()

    def draw_iris(self, painter: QPainter):
        if not self.visible_iris:
            return

        x1 = self.center.x()
        y1 = self.center.y()

        x2 = self.iris.center.x()
        y2 = self.iris.center.y()

        bounding_width = self.radiusX - self.iris.radiusX
        bounding_height = self.radiusY - self.iris.radiusY

        # Установим размер ограничивающего эллипса, он будет в процентах от размера глаз
        bounding_width = percent_number(bounding_width, 80)
        bounding_height = percent_number(bounding_height, 80)

        bounding_ellipse = Ellipse(
            self.center.x(), self.center.y(), bounding_width, bounding_height
        )

        a = pow(abs(x1 - x2), 2) + pow(abs(y1 - y2), 2)
        b = pow(self.radiusX, 2) - pow(
            percent_number(self.radiusX - self.iris.radiusX, 130), 2
        )
        if a >= b:
            line = Line(
                self.center.x(),
                self.center.y(),
                self.iris.center.x(),
                self.iris.center.y(),
            )
            result = ResultCrossLineAndEllipse()

            if is_ellipse_and_direct(bounding_ellipse, line, result):
                # TODO:
                result.x1 = int(result.x1)
                result.y1 = int(result.y1)
                result.x2 = int(result.x2)
                result.y2 = int(result.y2)

                if self.center.x() == self.iris.center.x():
                    if self.center.y() < self.iris.center.y():
                        self.iris.center.setX(result.x1)
                        self.iris.center.setY(result.y1)
                    else:
                        self.iris.center.setX(result.x2)
                        self.iris.center.setY(result.y2)

                elif self.center.x() > self.iris.center.x():
                    self.iris.center.setX(result.x1)
                    self.iris.center.setY(result.y1)

                elif self.center.x() < self.iris.center.x():
                    self.iris.center.setX(result.x2)
                    self.iris.center.setY(result.y2)

        painter.save()
        painter.translate(self.iris.center.x(), self.iris.center.y())

        painter.setBrush(self.iris.brush)
        painter.setPen(self.iris.pen)

        painter.drawEllipse(QPoint(0, 0), self.iris.radiusX, self.iris.radiusY)

        painter.restore()

    def draw_pupil(self, painter: QPainter):
        if not self.visible_pupil:
            return

        painter.save()
        painter.translate(self.iris.center.x(), self.iris.center.y())

        painter.setBrush(self.pupil.brush)
        painter.setPen(self.pupil.pen)

        painter.drawEllipse(QPoint(0, 0), self.pupil.radiusX, self.pupil.radiusY)
        painter.restore()
