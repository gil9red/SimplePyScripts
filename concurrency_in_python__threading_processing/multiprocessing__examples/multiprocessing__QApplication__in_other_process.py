#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def go(name):
    from PyQt5.Qt import QApplication, Qt, QLabel
    app = QApplication([])

    mw = QLabel()
    mw.setAlignment(Qt.AlignCenter)
    mw.setMinimumSize(150, 50)
    mw.setText('Hello, ' + name)
    mw.show()

    app.exec()


if __name__ == '__main__':
    from multiprocessing import Process
    p = Process(target=go, args=('bob',))
    p.start()

    # Необязательно в данном случае -- главный поток все-равно закроется после дочернего
    # p.join()
