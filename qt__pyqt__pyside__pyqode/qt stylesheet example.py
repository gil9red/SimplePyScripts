#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5 import Qt


app = Qt.QApplication([])

w = Qt.QListWidget()
w.addItems(['item #{}'.format(_) for _ in range(100)])
w.setStyleSheet("""
QScrollBar:vertical {
    border: 2px solid grey;
    background: #32CC99;
}
""")

w.show()

app.exec()
