#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QWidget


app = QApplication([])

mw = QWidget()

rect = mw.frameGeometry()
# This is where QDesktopWidget is used
center = app.desktop().availableGeometry().center()
rect.moveCenter(center)
mw.move(rect.topLeft())

mw.show()

app.exec()
