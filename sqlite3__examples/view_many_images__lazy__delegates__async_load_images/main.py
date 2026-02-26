#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery

from db import DB_FILE_NAME
from utils.FileListModel import FileListModel
from utils.ListImagesWidget import ListImagesWidget


ICON_WIDTH, ICON_HEIGHT = 128, 128
IMAGE_CACHE = dict()


class SqlQueryModel(QSqlQueryModel):
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> object:
        if role == Qt.ToolTipRole:
            return index.model().data(index.model().index(index.row(), 1))

        return super().data(index, role)


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        query = QSqlQuery("SELECT COUNT(*) FROM File")
        query.first()
        self.total_rows_sql = query.value(0)

        self.model_sql = SqlQueryModel()
        self.model_sql.rowsInserted.connect(self._on_added_new_items)
        self.model_sql.modelReset.connect(self._on_added_new_items)
        self.model_sql.setHeaderData(0, Qt.Horizontal, "ID")
        self.model_sql.setHeaderData(1, Qt.Horizontal, "FILE_NAME")

        self.list_view_sql = ListImagesWidget(
            ICON_WIDTH, ICON_HEIGHT, IMAGE_CACHE, file_name_index=1
        )
        self.list_view_sql.setModel(self.model_sql)

        list_files = []
        query = QSqlQuery("SELECT file_name FROM File")
        while query.next():
            file_name = query.value(0)
            list_files.append(file_name)

        self.model_files = FileListModel(batch_size=256)
        self.model_files.numberPopulated.connect(self._on_added_new_items)

        self.list_view_files = ListImagesWidget(
            ICON_WIDTH, ICON_HEIGHT, IMAGE_CACHE, file_name_index=0
        )
        self.list_view_files.setModel(self.model_files)

        self.model_sql.setQuery("SELECT id, file_name FROM File")
        self.model_files.setFileList(list_files)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("SQL:"))
        layout.addWidget(self.list_view_sql)
        layout.addWidget(QLabel("FILES:"))
        layout.addWidget(self.list_view_files)

        self.setLayout(layout)

    def _on_added_new_items(self) -> None:
        self.setWindowTitle(
            f"Items. "
            f"SQL: {self.model_sql.rowCount()} / {self.total_rows_sql} ({self.model_sql.rowCount() / self.total_rows_sql:.1%}) | "
            f"FILES: {self.model_files.rowCount()} / {self.total_rows_sql} ({self.model_files.rowCount() / self.total_rows_sql:.1%})"
        )


if __name__ == "__main__":
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(DB_FILE_NAME)
    if not db.open():
        raise Exception(db.lastError().text())

    app = QApplication([])

    mw = MainWindow()
    mw.move(100, 100)
    mw.resize(800, 600)
    mw.show()

    app.exec()
