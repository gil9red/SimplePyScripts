#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QFontMetrics
from PyQt5.QtCore import Qt


class ElidedLabel(QLabel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setMinimumWidth(50)
    
    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        metrics = QFontMetrics(self.font())
        elided_text = metrics.elidedText(self.text(), Qt.ElideRight, self.width())

        painter.drawText(self.rect(), self.alignment(), elided_text)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFont

    app = QApplication([])

    mw = ElidedLabel("abc123" * 100)
    mw.setFont(QFont("Arial", 20))
    mw.resize(100, 100)
    mw.show()

    app.exec()
