#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.Qt import QApplication, QLabel

app = QApplication([])

mw = QLabel()
mw.setText('<i>Hello</i> <b>World</b><i><b>!!!</b><i>')
mw.show()

app.exec()
