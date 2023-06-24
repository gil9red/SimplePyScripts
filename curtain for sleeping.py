#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Программа при клике на кнопку разворачивается на весь экран, закрашивается черным цветом. При
движении мышки, возвращается обратно в привычное состояние.
"""


try:
    from PyQt5.QtWidgets import (
        QWidget,
        QVBoxLayout,
        QPushButton,
        QSizePolicy,
        QApplication,
    )
    from PyQt5.QtGui import QPainter
    from PyQt5.QtCore import Qt, QTimer

except ImportError:
    from PyQt4.QtGui import (
        QWidget,
        QPainter,
        QVBoxLayout,
        QPushButton,
        QSizePolicy,
        QApplication,
    )
    from PyQt4.QtCore import Qt, QTimer


class CurtainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Curtain for sleeping")

        self._flags = self.windowFlags()

        self._activate_button = QPushButton("Activate curtain for sleeping")
        self._activate_button.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self._activate_button.clicked.connect(self._activate)

        # Таймер не дает, в течении 2 секунд, движением мышки вернуть окно в нормальный вид
        # Это сделано чтобы после клика на разворачивание во весь экран случайно оно не было возвращено обратно
        # в нормальное состояние
        self._timer_block_normal = QTimer()
        self._timer_block_normal.setSingleShot(True)
        self._timer_block_normal.setInterval(2000)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._activate_button)
        self.setLayout(layout)

        self.setMouseTracking(True)

    def _activate(self, _):
        self.showFullScreen()

    def showNormal(self):
        self._activate_button.show()
        self.unsetCursor()

        super().showNormal()

        # Восстановление старых флагов
        self.setWindowFlags(self._flags)
        self.show()

    def showFullScreen(self):
        self._activate_button.hide()
        self.setCursor(Qt.BlankCursor)
        self._timer_block_normal.start()

        # Установка флага Поверх всех окон
        self.setWindowFlags(self._flags | Qt.WindowStaysOnTopHint)

        super().showFullScreen()

    def mouseMoveEvent(self, event):
        if not self._timer_block_normal.isActive() and self.isFullScreen():
            self.showNormal()

        super().mouseMoveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(Qt.black)
        painter.setPen(Qt.black)
        painter.drawRect(self.rect())


app = QApplication([])

widget = CurtainWidget()
widget.resize(200, 200)
widget.show()

app.exec()
