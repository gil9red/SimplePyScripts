#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from typing import Callable

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
    QAction,
)


def copy_to_clipboard(value: str):
    QApplication.clipboard().setText(value)


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

    def _open_context_menu(
        self,
        table: QTableView,
        p: QPoint,
        get_additional_actions_func: Callable[[QTableView, int], list[QAction]] = None,
    ):
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

            idx: QModelIndex = model.index(row, column)
            value: str = str(model.data(idx))

            menu.addAction(
                f'Copy "{title}"',
                lambda value=value: copy_to_clipboard(value),
            )

        if get_additional_actions_func:
            if actions := get_additional_actions_func(table, row):
                menu.addSeparator()
                menu.addActions(actions)

        menu.exec(table.viewport().mapToGlobal(p))

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

    def _custom_menu_requested(self, p: QPoint):
        table: QTableView = self.sender()

        def _get_additional_actions(table: QTableView, row: int) -> list[QAction]:
            model = table.model()
            idx = model.index(row, 1)

            url: str = str(model.data(idx))

            action_url = QAction("Open URL")
            action_url.triggered.connect(lambda: os.startfile(url))

            return [action_url]

        self._open_context_menu(table, p, _get_additional_actions)


if __name__ == "__main__":
    app = QApplication([])

    w = MainWindow()
    w.resize(600, 500)
    w.show()

    app.exec()
