#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *

except:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *


class Widget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Table")

        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

    def fill(self):
        self.table_widget.clear()

        labels = ["ID", "NAME", "PRICE"]

        self.table_widget.setColumnCount(len(labels))
        self.table_widget.setHorizontalHeaderLabels(labels)

        with sqlite3.connect("games.sqlite") as connect:
            for id_, name, price in connect.execute(
                "SELECT id, name, price FROM Game WHERE kind = 'Finished'"
            ):
                row = self.table_widget.rowCount()
                self.table_widget.setRowCount(row + 1)

                self.table_widget.setItem(row, 0, QTableWidgetItem(str(id_)))
                self.table_widget.setItem(row, 1, QTableWidgetItem(name))
                self.table_widget.setItem(row, 2, QTableWidgetItem(price))


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.show()
    w.fill()

    app.exec()
