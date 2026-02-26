#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from multiprocessing import Process

import tkinter as tk
from PyQt5.Qt import QApplication, Qt, QLabel


def go_qt(name) -> None:
    app = QApplication([])

    mw = QLabel()
    mw.setAlignment(Qt.AlignCenter)
    mw.setMinimumSize(150, 50)
    mw.setText("Hello, " + name)
    mw.show()

    app.exec()


def go_tk(name) -> None:
    app = tk.Tk()
    app.minsize(150, 50)

    mw = tk.Label(app, text="Hello, " + name)
    mw.pack(fill="both", expand=True)

    app.mainloop()


def create_qt() -> None:
    p = Process(target=go_qt, args=("Qt",))
    p.start()


def create_tk() -> None:
    p = Process(target=go_tk, args=("Tk",))
    p.start()


if __name__ == "__main__":
    from PyQt5.Qt import QPushButton, QWidget, QVBoxLayout

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
