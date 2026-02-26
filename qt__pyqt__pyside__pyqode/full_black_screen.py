#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QTimer


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setMouseTracking(True)

        self._enabledClose = False
        QTimer.singleShot(5000, self._setEnabledClose)

    def _setEnabledClose(self) -> None:
        self._enabledClose = True

    def mouseMoveEvent(self, event) -> None:
        if self._enabledClose:
            self.close()

    def mousePressEvent(self, event) -> None:
        if self._enabledClose:
            self.close()

    def keyPressEvent(self, event) -> None:
        if self._enabledClose:
            self.close()

    def paintEvent(self, event) -> None:
        color = Qt.black

        painter = QPainter(self)
        painter.setPen(color)
        painter.setBrush(color)

        painter.drawRect(self.rect())


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    # mw.show()
    mw.showFullScreen()

    app.exec()
