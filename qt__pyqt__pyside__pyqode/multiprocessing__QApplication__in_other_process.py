#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from multiprocessing import Process
from PyQt5 import Qt


def go(name):
    app = Qt.QApplication([])

    mw = Qt.QLabel()
    mw.setText('Hello, ' + name)
    mw.show()

    app.exec()


if __name__ == '__main__':
    p = Process(target=go, args=('bob',))
    p.start()
    p.join()
