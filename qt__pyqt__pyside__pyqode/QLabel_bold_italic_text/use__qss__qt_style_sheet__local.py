#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.Qt import QApplication, QLabel

app = QApplication([])

mw = QLabel()
mw.setText('Hello World!!!')
mw.setStyleSheet('font: bold italic')
mw.show()

app.exec()
