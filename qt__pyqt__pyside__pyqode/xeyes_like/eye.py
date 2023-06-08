#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass

from PyQt5.QtGui import QBrush, QPen, QPainter
from PyQt5.QtCore import QPoint, Qt

from support import USupport, UEllipse, ULine, UResultCrossLineAndEllipse, UIntersection


@dataclass
class EllipseObject:
    center: QPoint = QPoint(0, 0)
    radiusX: float = 0.0
    radiusY: float = 0.0

    brush: QBrush = Qt.black
    pen: QPen = QPen(Qt.black, 1.0)


@dataclass
class UIris(EllipseObject):
    """Радужка"""


@dataclass
class UPupil(EllipseObject):
    """Зрачок"""


@dataclass
class UEye(EllipseObject):
    """Глаз"""

    iris: UIris = UIris()
    pupil: UPupil = UPupil()

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

        boundingWidth = self.radiusX - self.iris.radiusX
        boundingHeight = self.radiusY - self.iris.radiusY

        # Установим размер ограничивающего эллипса, он будет в процентах от размера глаз
        boundingWidth = USupport.percentNumber(boundingWidth, 80)
        boundingHeight = USupport.percentNumber(boundingHeight, 80)

        boundingEllipse = UEllipse(
            self.center.x(), self.center.y(), boundingWidth, boundingHeight
        )

        a = pow(abs(x1 - x2), 2) + pow(abs(y1 - y2), 2)
        b = pow(self.radiusX, 2) - pow(
            USupport.percentNumber(self.radiusX - self.iris.radiusX, 130), 2
        )
        if a >= b:
            line = ULine(
                self.center.x(),
                self.center.y(),
                self.iris.center.x(),
                self.iris.center.y(),
            )
            result = UResultCrossLineAndEllipse()

            if UIntersection.isEllipseAndDirect(boundingEllipse, line, result):
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
