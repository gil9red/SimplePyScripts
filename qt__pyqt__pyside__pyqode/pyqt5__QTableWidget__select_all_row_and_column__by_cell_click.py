#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QApplication
from PyQt5.QtCore import QItemSelectionModel


class Widget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Table")

        self.table_widget = QTableWidget()
        self.table_widget.cellClicked.connect(self._on_cell_clicked)

        self.setCentralWidget(self.table_widget)

    def _on_cell_clicked(self, row, col):
        selection_model = self.table_widget.selectionModel()
        selection_model.clear()

        for i in range(self.table_widget.rowCount()):
            for j in range(self.table_widget.columnCount()):
                if i == row or j == col:
                    item = self.table_widget.item(i, j)
                    index = self.table_widget.indexFromItem(item)

                    selection_model.select(index, QItemSelectionModel.Select)

    def fill(self):
        self.table_widget.clear()

        labels = ["ID", "NAME", "PRICE"]

        self.table_widget.setColumnCount(len(labels))
        self.table_widget.setHorizontalHeaderLabels(labels)

        for id_, name, price in [
            ["1", "name_1", "price_1"],
            ["2", "name_2", "price_2"],
            ["3", "name_3", "price_3"],
        ]:
            row = self.table_widget.rowCount()
            self.table_widget.setRowCount(row + 1)

            self.table_widget.setItem(row, 0, QTableWidgetItem(str(id_)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(price))


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.show()
    w.resize(400, 200)
    w.fill()

    app.exec()
