#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from multiprocessing import Pool
from PyQt5 import Qt


def go(name):
    app = Qt.QApplication([])

    mw = Qt.QLabel()
    mw.setText('Hello, ' + name)
    mw.show()

    app.exec()


if __name__ == '__main__':
    with Pool() as p:
        p.map(go, ['Alice', 'Bob', 'World'])
