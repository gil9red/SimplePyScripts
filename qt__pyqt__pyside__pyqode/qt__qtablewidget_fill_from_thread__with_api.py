#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/a/806056/201445


import time

import requests

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal as Signal


class CheckNewData(QThread):
    about_new_data = Signal(dict)

    def run(self) -> None:
        while True:
            # API - start
            rs = requests.get(
                "https://bittrex.com/api/v1.1/public/getmarketsummary?market=BTC-TRX"
            )
            data = rs.json()
            print(data)
            # API - end

            self.about_new_data.emit(data)

            time.sleep(60)


class Sheet(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setMinimumSize(QSize(600, 300))
        self.setWindowTitle("Table_title")

        central_widget = QWidget()

        grid_layout = QGridLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(["A", "B", "C"])
        self.table.setVerticalHeaderLabels(["1", "TRX", "3"])

        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)

        self.thread = CheckNewData()
        self.thread.about_new_data.connect(self.update_table)
        self.thread.start()

        grid_layout.addWidget(self.table, 0, 0)

        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

    def update_table(self, data) -> None:
        print("update_table:", data)

        k = data["result"][0]["Last"]
        btctrx = "%.8f" % k

        # Удаляем строки таблицы
        while self.table.rowCount():
            self.table.removeRow(0)

        self.table.setRowCount(3)

        self.table.setItem(0, 0, QTableWidgetItem())
        self.table.setItem(0, 1, QTableWidgetItem())
        self.table.setItem(0, 2, QTableWidgetItem())
        self.table.setItem(1, 0, QTableWidgetItem(btctrx))

        self.table.resizeColumnsToContents()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    mw = Sheet()
    mw.show()

    sys.exit(app.exec())
