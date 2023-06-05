#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


app = Qt.QApplication([])

button = Qt.QToolButton()
button.setIcon(Qt.QIcon("img.png"))
button.setAutoRaise(True)
button.setMinimumSize(40, 50)
button.setIconSize(button.minimumSize())

layout = Qt.QVBoxLayout()
layout.addWidget(Qt.QLabel("Example:"))
layout.addWidget(button)

central = Qt.QWidget()
central.setStyleSheet("background-color: green;")
central.setLayout(layout)

mw = Qt.QMainWindow()
mw.setCentralWidget(central)
mw.show()

app.exec()
