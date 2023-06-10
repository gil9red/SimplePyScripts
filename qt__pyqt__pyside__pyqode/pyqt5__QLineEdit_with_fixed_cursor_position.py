#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


app = Qt.QApplication([])

le = Qt.QLineEdit()
le.textEdited.connect(lambda _: le.setCursorPosition(1))
le.show()

app.exec()
