#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp


app = QApplication([])

mw = QLineEdit()
mw.setText("1.3.6.1.2.1.25.1.1.0")
mw.setValidator(QRegExpValidator(QRegExp(r"\d+(\.\d+)+")))
mw.show()

app.exec()
