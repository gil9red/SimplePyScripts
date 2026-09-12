#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal, QVariant


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/f49a0c3462176ccc34bf31dffbe6fd88d1baa0bd/qt__pyqt__pyside__pyqode/lazy__qtwidgets_itemviews_fetchmore_example__QAbstractListModel.py#L19
class FileListModel(QAbstractListModel):
    numberPopulated = pyqtSignal(int)

    def __init__(self, batch_size=50, parent=None):
        super().__init__(parent)

        self.total_file_list = []
        self.current_file_count = 0
        self.batch_size = batch_size

    def rowCount(self, parent: QModelIndex = None) -> int:
        return self.current_file_count

    def data(self, index: QModelIndex, role=Qt.DisplayRole) -> QVariant:
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self.total_file_list) or index.row() < 0:
            return QVariant()

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            return self.total_file_list[index.row()]

        # elif role == Qt.BackgroundRole:
        #     batch = (index.row() // self.batch_size) % 2
        #     if batch == 0:
        #         return QApplication.instance().palette().base()
        #     else:
        #         return QApplication.instance().palette().alternateBase()

        return QVariant()

    def canFetchMore(self, parent: QModelIndex = None) -> bool:
        return self.current_file_count < len(self.total_file_list)

    def fetchMore(self, parent: QModelIndex = None):
        remainder = len(self.total_file_list) - self.current_file_count
        itemsToFetch = min(self.batch_size, remainder)
        if itemsToFetch <= 0:
            return

        self.beginInsertRows(
            QModelIndex(), self.current_file_count, self.current_file_count + itemsToFetch - 1
        )

        self.current_file_count += itemsToFetch

        self.endInsertRows()

        self.numberPopulated.emit(itemsToFetch)

    def set_total_file_list(self, fileList: list):
        self.beginResetModel()

        self.total_file_list = fileList
        self.current_file_count = 0
        self.numberPopulated.emit(0)

        self.endResetModel()
