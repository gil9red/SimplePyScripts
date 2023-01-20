#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPaintEvent, QPainter, QBrush, QPen
from PyQt5.QtCore import QPoint, Qt

from eye import UEye, UIris, UPupil
from support import USupport, minimalWidthEye


class UEyeWidget(QWidget):
    eye: UEye = UEye(
        brush=Qt.white,
        pen=QPen(Qt.black, 2.0),
        iris=UIris(
            brush=Qt.black,
            pen=QPen(Qt.black, 1.0),
        ),
        pupil=UPupil(
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

        self.setDiameter(minimalWidthEye)

    # def setBrush(self, brush: QBrush):
    #     self.eye.brush = brush

    def setDiameter(self, diameter: int):
        self.setFixedSize(diameter, diameter)

    # def setBrush(const QBrush brush)
    # def setPen(const QPen pen)
    # QPoint center()
    # float radiusX()
    # float radiusY()
    # QBrush brush()
    # QPen pen()
    # 
    # 
    # def setBrushIris(const QBrush brush)
    # def setPenIris(const QPen pen)
    # QPoint centerIris()
    # def setRadiusXIris(float radius)
    # def setRadiusYIris(float radius)
    # float radiusXIris()
    # float radiusYIris()
    # QBrush brushIris()
    # QPen penIris()
    # 
    # 
    # def setBrushPupil(const QBrush brush)
    # def setPenPupil(const QPen pen)
    # QPoint centerPupil()
    # def setRadiusXPupil(float radius)
    # def setRadiusYPupil(float radius)
    # float radiusXPupil()
    # float radiusYPupil()
    # QBrush brushPupil()
    # QPen penPupil()
    # 
    # int percentIrisRadiusX()
    # int percentIrisRadiusY()
    # 
    # int percentPupilRadiusX()
    # int percentPupilRadiusY()

    def lookThere(self, position: QPoint):
        self.positionLook = self.mapFromGlobal(position)
        self.update()

    # def setPercentIrisRadiusX(int percent)
    # def setPercentIrisRadiusY(int percent)
    #
    # def setPercentPupilRadiusX(int percent)
    # def setPercentPupilRadiusY(int percent)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
    
        indent = 3
    
        # По размерам окна определим примерно размер глаз
        # расчет будет по высоте и ширине
        rXFromWidth: float = (self.width() - indent * 2) / 2
        rYFromHeigth: float = (self.height() - indent * 2) / 2
    
        radiusXEye: float = min(rXFromWidth, rYFromHeigth)
        radiusYEye: float = radiusXEye
    
        radiusXIris: float = USupport.percentNumber(radiusXEye, self.d_percentIrisRadiusX)
        radiusYIris: float = USupport.percentNumber(radiusYEye, self.d_percentIrisRadiusY)
    
        radiusXPupil: float = USupport.percentNumber(radiusXIris, self.d_percentPupilRadiusX)
        radiusYPupil: float = USupport.percentNumber(radiusYIris, self.d_percentPupilRadiusY)
    
        x: int = int(radiusXEye + indent)
        y: int = int(radiusYEye + indent)
    
        self.eye.radiusX = radiusXEye
        self.eye.radiusY = radiusYEye
        self.eye.center = QPoint(x, y)

        # Радужка глаза
        iris = self.eye.iris
        iris.radiusX = radiusXIris
        iris.radiusY = radiusYIris
        iris.center = self.positionLook
        # Радужка глаза
    
        # Зрачок глаза
        pupil = self.eye.pupil
        pupil.radiusX = radiusXPupil
        pupil.radiusY = radiusYPupil
        # Зрачок глаза
    
        self.eye.draw(painter)
