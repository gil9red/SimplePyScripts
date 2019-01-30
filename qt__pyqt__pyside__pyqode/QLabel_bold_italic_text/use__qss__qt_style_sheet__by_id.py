#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.Qt import QApplication, QLabel

app = QApplication([])
app.setStyleSheet('#welcome { font: bold italic }')

mw = QLabel()
mw.setObjectName('welcome')
mw.setText('Hello World!!!')
mw.show()

app.exec()
