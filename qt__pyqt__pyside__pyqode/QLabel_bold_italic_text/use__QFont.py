#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.Qt import QApplication, QLabel

app = QApplication([])

mw = QLabel()

font = mw.font()
font.setItalic(True)
font.setBold(True)
mw.setFont(font)

mw.setText('Hello World!!!')
mw.show()

app.exec()
