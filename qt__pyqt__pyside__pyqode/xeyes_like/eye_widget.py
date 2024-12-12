#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPaintEvent, QPainter, QPen
from PyQt5.QtCore import QPoint, Qt

from eye import Eye, Iris, Pupil
from support import MINIMAL_WIDTH_EYE, percent_number


class EyeWidget(QWidget):
    eye: Eye = Eye(
        brush=Qt.white,
        pen=QPen(Qt.black, 2.0),
        iris=Iris(
            brush=Qt.black,
            pen=QPen(Qt.black, 1.0),
        ),
        pupil=Pupil(
            brush=Qt.black,
            pen=QPen(Qt.white, 1.0),
        ),
    )

    d_percentIrisRadiusX: int = 30
    d_percentIrisRadiusY: int = 30

    d_percentPupilRadiusX: int = 55
    d_percentPupilRadiusY: int = 55

    positionLook: QPoint = QPoint(0, 0)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.set_diameter(MINIMAL_WIDTH_EYE)

    def set_diameter(self, diameter: int):
        self.setFixedSize(diameter, diameter)

    def look_there(self, position: QPoint):
        self.positionLook = self.mapFromGlobal(position)
        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        indent = 3

        # По размерам окна определим примерно размер глаз
        # расчет будет по высоте и ширине
        r_x_from_width: float = (self.width() - indent * 2) / 2
        r_y_from_heigth: float = (self.height() - indent * 2) / 2

        radius_x_eye: float = min(r_x_from_width, r_y_from_heigth)
        radius_y_eye: float = radius_x_eye

        radius_x_iris: float = percent_number(radius_x_eye, self.d_percentIrisRadiusX)
        radius_y_iris: float = percent_number(radius_y_eye, self.d_percentIrisRadiusY)

        radius_x_pupil: float = percent_number(
            radius_x_iris, self.d_percentPupilRadiusX
        )
        radius_y_pupil: float = percent_number(
            radius_y_iris, self.d_percentPupilRadiusY
        )

        x: int = int(radius_x_eye + indent)
        y: int = int(radius_y_eye + indent)

        self.eye.radiusX = radius_x_eye
        self.eye.radiusY = radius_y_eye
        self.eye.center = QPoint(x, y)

        # Радужка глаза
        iris = self.eye.iris
        iris.radiusX = radius_x_iris
        iris.radiusY = radius_y_iris
        iris.center = self.positionLook

        # Зрачок глаза
        pupil = self.eye.pupil
        pupil.radiusX = radius_x_pupil
        pupil.radiusY = radius_y_pupil

        self.eye.draw(painter)
