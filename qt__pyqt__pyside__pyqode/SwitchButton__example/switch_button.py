#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://stackoverflow.com/a/51023362/5909792


from PyQt5 import QtWidgets, QtCore, QtGui


class SwitchButton(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None, w1="Yes", l1=12, w2="No", l2=33, width=60):
        super(SwitchButton, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.__labeloff = QtWidgets.QLabel(self)
        self.__labeloff.setText(w2)
        self.__labeloff.setStyleSheet("""color: rgb(120, 120, 120); font-weight: bold;""")
        self.__background  = Background(self)
        self.__labelon = QtWidgets.QLabel(self)
        self.__labelon.setText(w1)
        self.__labelon.setStyleSheet("""color: rgb(255, 255, 255); font-weight: bold;""")
        self.__circle      = Circle(self)
        self.__circlemove  = None
        self.__ellipsemove = None
        self.__enabled     = True
        self.__duration    = 100
        self.__value       = False
        self.setFixedSize(width, 24)

        self.__background.resize(20, 20)
        self.__background.move(2, 2)
        self.__circle.move(2, 2)
        self.__labelon.move(l1, 5)
        self.__labeloff.move(l2, 5)

    def checked(self) -> bool:
        return self.__value

    def valueText(self) -> str:
        return self.__labelon.text() if self.checked() else self.__labeloff.text()

    def setDuration(self, time):
        self.__duration = time

    def mousePressEvent(self, event):
        if not self.__enabled:
            return

        self.__circlemove = QtCore.QPropertyAnimation(self.__circle, b"pos")
        self.__circlemove.setDuration(self.__duration)

        self.__ellipsemove = QtCore.QPropertyAnimation(self.__background, b"size")
        self.__ellipsemove.setDuration(self.__duration)

        xs = 2
        y  = 2
        xf = self.width()-22
        hback = 20
        isize = QtCore.QSize(hback, hback)
        bsize = QtCore.QSize(self.width()-4, hback)
        if self.__value:
            xf = 2
            xs = self.width()-22
            bsize = QtCore.QSize(hback, hback)
            isize = QtCore.QSize(self.width()-4, hback)

        self.__circlemove.setStartValue(QtCore.QPoint(xs, y))
        self.__circlemove.setEndValue(QtCore.QPoint(xf, y))

        self.__ellipsemove.setStartValue(isize)
        self.__ellipsemove.setEndValue(bsize)

        self.__circlemove.start()
        self.__ellipsemove.start()
        self.__value = not self.__value

        self.clicked.emit(self.checked())

    def paintEvent(self, event):
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        pen = QtGui.QPen(QtCore.Qt.NoPen)
        qp.setPen(pen)
        qp.setBrush(QtGui.QColor(120, 120, 120))
        qp.drawRoundedRect(0, 0, s.width(), s.height(), 12, 12)
        lg = QtGui.QLinearGradient(35, 30, 35, 0)
        lg.setColorAt(0, QtGui.QColor(210, 210, 210, 255))
        lg.setColorAt(0.25, QtGui.QColor(255, 255, 255, 255))
        lg.setColorAt(0.82, QtGui.QColor(255, 255, 255, 255))
        lg.setColorAt(1, QtGui.QColor(210, 210, 210, 255))
        qp.setBrush(lg)
        qp.drawRoundedRect(1, 1, s.width()-2, s.height()-2, 10, 10)

        qp.setBrush(QtGui.QColor(210, 210, 210))
        qp.drawRoundedRect(2, 2, s.width() - 4, s.height() - 4, 10, 10)

        if self.__enabled:
            lg = QtGui.QLinearGradient(50, 30, 35, 0)
            lg.setColorAt(0, QtGui.QColor(230, 230, 230, 255))
            lg.setColorAt(0.25, QtGui.QColor(255, 255, 255, 255))
            lg.setColorAt(0.82, QtGui.QColor(255, 255, 255, 255))
            lg.setColorAt(1, QtGui.QColor(230, 230, 230, 255))
            qp.setBrush(lg)
            qp.drawRoundedRect(3, 3, s.width() - 6, s.height() - 6, 7, 7)
        else:
            lg = QtGui.QLinearGradient(50, 30, 35, 0)
            lg.setColorAt(0, QtGui.QColor(200, 200, 200, 255))
            lg.setColorAt(0.25, QtGui.QColor(230, 230, 230, 255))
            lg.setColorAt(0.82, QtGui.QColor(230, 230, 230, 255))
            lg.setColorAt(1, QtGui.QColor(200, 200, 200, 255))
            qp.setBrush(lg)
            qp.drawRoundedRect(3, 3, s.width() - 6, s.height() - 6, 7, 7)
        qp.end()


class Circle(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Circle, self).__init__(parent)
        self.__enabled = True
        self.setFixedSize(20, 20)

    def paintEvent(self, event):
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(120, 120, 120))
        qp.drawEllipse(0, 0, 20, 20)
        rg = QtGui.QRadialGradient(int(self.width() / 2), int(self.height() / 2), 12)
        rg.setColorAt(0, QtGui.QColor(255, 255, 255))
        rg.setColorAt(0.6, QtGui.QColor(255, 255, 255))
        rg.setColorAt(1, QtGui.QColor(205, 205, 205))
        qp.setBrush(QtGui.QBrush(rg))
        qp.drawEllipse(1,1, 18, 18)

        qp.setBrush(QtGui.QColor(210, 210, 210))
        qp.drawEllipse(2, 2, 16, 16)

        if self.__enabled:
            lg = QtGui.QLinearGradient(3, 18,20, 4)
            lg.setColorAt(0, QtGui.QColor(255, 255, 255, 255))
            lg.setColorAt(0.55, QtGui.QColor(230, 230, 230, 255))
            lg.setColorAt(0.72, QtGui.QColor(255, 255, 255, 255))
            lg.setColorAt(1, QtGui.QColor(255, 255, 255, 255))
            qp.setBrush(lg)
            qp.drawEllipse(3,3, 14, 14)
        else:
            lg = QtGui.QLinearGradient(3, 18, 20, 4)
            lg.setColorAt(0, QtGui.QColor(230, 230, 230))
            lg.setColorAt(0.55, QtGui.QColor(210, 210, 210))
            lg.setColorAt(0.72, QtGui.QColor(230, 230, 230))
            lg.setColorAt(1, QtGui.QColor(230, 230, 230))
            qp.setBrush(lg)
            qp.drawEllipse(3, 3, 14, 14)
        qp.end()


class Background(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Background, self).__init__(parent)
        self.__enabled = True
        self.setFixedHeight(20)

    def paintEvent(self, event):
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        pen = QtGui.QPen(QtCore.Qt.NoPen)
        qp.setPen(pen)
        qp.setBrush(QtGui.QColor(154,205,50))
        if self.__enabled:
            qp.setBrush(QtGui.QColor(154, 190, 50))
            qp.drawRoundedRect(0, 0, s.width(), s.height(), 10, 10)

            lg = QtGui.QLinearGradient(0, 25, 70, 0)
            lg.setColorAt(0, QtGui.QColor(154, 184, 50))
            lg.setColorAt(0.35, QtGui.QColor(154, 210, 50))
            lg.setColorAt(0.85, QtGui.QColor(154, 184, 50))
            qp.setBrush(lg)
            qp.drawRoundedRect(1, 1, s.width() - 2, s.height() - 2, 8, 8)
        else:
            qp.setBrush(QtGui.QColor(150, 150, 150))
            qp.drawRoundedRect(0, 0, s.width(), s.height(), 10, 10)

            lg = QtGui.QLinearGradient(5, 25, 60, 0)
            lg.setColorAt(0, QtGui.QColor(190, 190, 190))
            lg.setColorAt(0.35, QtGui.QColor(230, 230, 230))
            lg.setColorAt(0.85, QtGui.QColor(190, 190, 190))
            qp.setBrush(lg)
            qp.drawRoundedRect(1, 1, s.width() - 2, s.height() - 2, 8, 8)
        qp.end()
