#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from multiprocessing import Process
from multiprocessing__QApplication__in_other_process import go as go_qt
from multiprocessing__Tkinter__in_other_process import go as go_tk


def create_qt():
    p = Process(target=go_qt, args=("Qt",))
    p.start()


def create_tk():
    p = Process(target=go_tk, args=("Tk",))
    p.start()


if __name__ == "__main__":
    from PyQt5.Qt import QApplication, QPushButton, QWidget, QVBoxLayout

    app = QApplication([])

    button_qt = QPushButton("Create Qt")
    button_qt.clicked.connect(create_qt)

    button_tk = QPushButton("Create Tk")
    button_tk.clicked.connect(create_tk)

    layout = QVBoxLayout()
    layout.addWidget(button_qt)
    layout.addWidget(button_tk)

    mw = QWidget()
    mw.setLayout(layout)
    mw.show()

    app.exec()
