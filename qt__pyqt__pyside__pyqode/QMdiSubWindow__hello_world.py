#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMdiSubWindow,
    QMdiArea,
    QTextEdit,
    QPushButton,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.sub_window_1 = QMdiSubWindow()
        self.sub_window_1.setWidget(QTextEdit("<h1>Hello World!</h1>"))

        self.sub_window_2 = QMdiSubWindow()
        self.sub_window_2.setWidget(QPushButton("Click!"))

        self.mdi_area = QMdiArea()
        self.mdi_area.addSubWindow(self.sub_window_1)
        self.mdi_area.addSubWindow(self.sub_window_2)

        self.setCentralWidget(self.mdi_area)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
