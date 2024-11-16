#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from PyQt5.QtCore import QPoint, Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QTableView,
    QMenu,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        header_labels = ["NAME", "URL"]

        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QTableView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QTableView.SelectRows)
        self.table_widget.setSelectionMode(QTableView.SingleSelection)
        self.table_widget.setColumnCount(len(header_labels))
        self.table_widget.setHorizontalHeaderLabels(header_labels)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(
            self._custom_menu_requested
        )

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(header_labels)

        self.table_view = QTableView()
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setModel(self.model)
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self._custom_menu_requested)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.table_view)
        main_layout.addWidget(self.table_widget)

        self.fill_tables()

    def fill_tables(self):
        self.model.appendRow(
            [QStandardItem("rutube"), QStandardItem("https://rutube.ru/")]
        )
        self.model.appendRow(
            [QStandardItem("yandex"), QStandardItem("https://yandex.ru/")]
        )
        self.model.appendRow(
            [QStandardItem("youtube"), QStandardItem("https://www.youtube.com")]
        )
        self.model.appendRow(
            [QStandardItem("google"), QStandardItem("https://google.com/")]
        )

        self.table_widget.setRowCount(self.model.rowCount())
        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                text = self.model.item(row, column).text()
                self.table_widget.setItem(row, column, QTableWidgetItem(text))

    def _get_url(self, table, row: int) -> str:
        model = table.model()

        idx = model.index(row, 1)
        return model.data(idx)

    def _custom_menu_requested(self, p: QPoint):
        table = self.sender()

        index: QModelIndex = table.indexAt(p)
        if not index.isValid():
            return

        menu = QMenu(self)
        menu.addAction(table.__class__.__name__).setEnabled(False)
        menu.addSeparator()

        row: int = index.row()
        model = table.model()

        for column in range(model.columnCount()):
            title = model.headerData(column, Qt.Horizontal)

            idx = model.index(row, column)
            value = model.data(idx)

            menu.addAction(
                f'Copy "{title}"',
                lambda value=value: QApplication.clipboard().setText(value),
            )

        url = self._get_url(table, row)
        if url:
            menu.addSeparator()
            menu.addAction("Open URL", lambda: os.startfile(url))

        menu.exec(table.viewport().mapToGlobal(p))


if __name__ == "__main__":
    app = QApplication([])

    w = MainWindow()
    w.resize(600, 500)
    w.show()

    app.exec()
