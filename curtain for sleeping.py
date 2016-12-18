#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Программа при клике на кнопку разворачивается на весь экран, закрашивается черным цветом. При
движении мышки, возвращается обратно в привычное состояние.
"""


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class CurtainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Curtain for sleeping')

        self._activate_button = QPushButton('Activate curtain for sleeping')
        self._activate_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._activate_button.clicked.connect(self._activate)

        layout = QVBoxLayout()
        layout.addWidget(self._activate_button)
        self.setLayout(layout)

        self.setMouseTracking(True)

    def _activate(self, _):
        self.showFullScreen()

    def showNormal(self):
        self._activate_button.show()
        self.unsetCursor()

        super().showNormal()

    def showFullScreen(self):
        self._activate_button.hide()
        self.setCursor(Qt.BlankCursor)

        super().showFullScreen()

    def mouseMoveEvent(self, event):
        if self.isFullScreen():
            self.showNormal()

        super().mouseMoveEvent(event)

    def paintEvent(self, event):
        if not self.isFullScreen():
            super().paintEvent(event)
            return

        painter = QPainter(self)
        painter.setBrush(Qt.black)
        painter.setPen(Qt.black)
        painter.drawRect(self.rect())


app = QApplication([])

widget = CurtainWidget()
widget.resize(200, 200)
widget.show()

app.exec()

