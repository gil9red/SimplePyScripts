#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QRect


app = QApplication([])

text = "Hello World!"

pixmap = QPixmap(180, 130)
pixmap.fill(Qt.white)

painter = QPainter(pixmap)
painter.setFont(QFont("Arial", 12))

rect = QRect(0, 0, 70, 50)
painter.drawRect(rect)
painter.drawText(rect, Qt.TextWordWrap, text)

rect = QRect(0, 60, 70, 50)
painter.drawRect(rect)
painter.drawText(rect, Qt.AlignLeft, text)

w = QLabel()
w.setPixmap(pixmap)
w.show()

app.exec()
