#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from multiprocessing import Process


def go_qt(name):
    from PyQt5 import Qt
    app = Qt.QApplication([])

    mw = Qt.QLabel()
    mw.setAlignment(Qt.Qt.AlignCenter)
    mw.setMinimumSize(150, 50)
    mw.setText('Hello, ' + name)
    mw.show()

    app.exec()


def go_tk(name):
    import tkinter as tk
    app = tk.Tk()
    app.minsize(150, 50)

    mw = tk.Label(app, text='Hello, ' + name)
    mw.pack(fill='both', expand=True)

    app.mainloop()


def create_qt():
    p = Process(target=go_qt, args=('Qt',))
    p.start()


def create_tk():
    p = Process(target=go_tk, args=('Tk',))
    p.start()


if __name__ == '__main__':
    from PyQt5 import Qt
    app = Qt.QApplication([])

    button_qt = Qt.QPushButton('Create Qt')
    button_qt.clicked.connect(create_qt)

    button_tk = Qt.QPushButton('Create Tk')
    button_tk.clicked.connect(create_tk)

    layout = Qt.QVBoxLayout()
    layout.addWidget(button_qt)
    layout.addWidget(button_tk)

    mw = Qt.QWidget()
    mw.setLayout(layout)
    mw.show()

    app.exec()
