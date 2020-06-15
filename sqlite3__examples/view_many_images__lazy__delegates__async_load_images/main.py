#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import (
    QApplication, QListView, QWidget, QVBoxLayout
)
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery

from db import DB_FILE_NAME
from utils.ThumbnailDelegate import ThumbnailDelegate


ICON_WIDTH, ICON_HEIGHT = 128, 128
IMAGE_CACHE = dict()


class SqlQueryModel(QSqlQueryModel):
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> object:
        if role == Qt.ToolTipRole:
            return index.model().data(
                index.model().index(index.row(), 1)
            )

        return super().data(index, role)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        query = QSqlQuery("SELECT COUNT(*) FROM File")
        query.first()
        self.total_rows = query.value(0)

        self.model = SqlQueryModel()
        self.model.rowsInserted.connect(self._on_added_new_items)
        self.model.modelReset.connect(self._on_added_new_items)
        self.model.setQuery("SELECT id, file_name FROM File")
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "FILE_NAME")

        self.list_view = QListView()
        self.list_view.setMovement(QListView.Static)
        self.list_view.setDragEnabled(False)
        self.list_view.setDragDropMode(QListView.NoDragDrop)
        self.list_view.setDropIndicatorShown(False)
        self.list_view.setViewMode(QListView.IconMode)
        self.list_view.setResizeMode(QListView.Adjust)
        self.list_view.setSpacing(5)
        self.list_view.setUniformItemSizes(True)
        self.list_view.setItemDelegate(
            ThumbnailDelegate(self.list_view, ICON_WIDTH, ICON_HEIGHT, IMAGE_CACHE)
        )
        self.list_view.setModel(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.list_view)

        self.setLayout(layout)

    def _on_added_new_items(self):
        self.setWindowTitle(
            f'Items: {self.model.rowCount()} / {self.total_rows} ({self.model.rowCount() / self.total_rows:.1%})'
        )


if __name__ == '__main__':
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(DB_FILE_NAME)
    if not db.open():
        raise Exception(db.lastError().text())

    app = QApplication([])

    mw = MainWindow()
    mw.move(100, 100)
    mw.resize(800, 600)
    mw.show()

    app.exec()
