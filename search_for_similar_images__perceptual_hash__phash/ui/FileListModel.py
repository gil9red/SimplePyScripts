#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal, QVariant


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/f49a0c3462176ccc34bf31dffbe6fd88d1baa0bd/qt__pyqt__pyside__pyqode/lazy__qtwidgets_itemviews_fetchmore_example__QAbstractListModel.py#L19
class FileListModel(QAbstractListModel):
    numberPopulated = pyqtSignal(int)

    IsMainRole = Qt.UserRole
    IsMatchedRole = Qt.UserRole + 1

    def __init__(self, batch_size=50, parent=None):
        super().__init__(parent)

        self.batch_size = batch_size

        self.fileList = []
        self.fileCount = 0

        self.main_file = None
        self.matched_files = []
        self.mark_matching = True

    def rowCount(self, parent: QModelIndex = None) -> int:
        return self.fileCount

    def data(self, index: QModelIndex, role=Qt.DisplayRole) -> QVariant:
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self.fileList) or index.row() < 0:
            return QVariant()

        file_name = self.fileList[index.row()]

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            return file_name

        if role in [self.IsMainRole, self.IsMatchedRole]:
            if self.mark_matching:
                if role == self.IsMainRole:
                    return self.main_file is not None and file_name == self.main_file
                else:
                    return file_name in self.matched_files

            else:
                return False

        # elif role == Qt.BackgroundRole:
        #     batch = (index.row() // self.batch_size) % 2
        #     if batch == 0:
        #         return QApplication.instance().palette().base()
        #     else:
        #         return QApplication.instance().palette().alternateBase()

        return QVariant()

    def canFetchMore(self, parent: QModelIndex = None) -> bool:
        return self.fileCount < len(self.fileList)

    def fetchMore(self, parent: QModelIndex = None):
        remainder = len(self.fileList) - self.fileCount
        itemsToFetch = min(self.batch_size, remainder)
        if itemsToFetch <= 0:
            return

        self.beginInsertRows(
            QModelIndex(), self.fileCount, self.fileCount + itemsToFetch - 1
        )

        self.fileCount += itemsToFetch

        self.endInsertRows()

        self.numberPopulated.emit(itemsToFetch)

    def set_file_list(self, fileList: list):
        self.beginResetModel()

        self.fileList = fileList
        self.fileCount = 0

        self.endResetModel()

    def set_matched_files(self, main_file: str, file_list: list):
        self.main_file = main_file

        self.matched_files.clear()
        self.matched_files.extend(file_list)

    def set_mark_matching(self, mark_matching: bool):
        self.mark_matching = mark_matching

    def get_index_by_file_name(self, file_name: str, column=0) -> QModelIndex:
        try:
            row = self.fileList.index(file_name)
            return self.index(row, column)
        except ValueError:
            pass

        return QModelIndex()
