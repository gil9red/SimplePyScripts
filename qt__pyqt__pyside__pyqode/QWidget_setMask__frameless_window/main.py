#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import QApplication, QPixmap, QLabel


app = QApplication([])

pix = QPixmap("pipe.png")

win = QLabel()
win.setPixmap(pix)
win.setMask(pix.mask())
win.show()

app.exec()
