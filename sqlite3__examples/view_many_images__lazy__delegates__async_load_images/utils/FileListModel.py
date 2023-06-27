#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal, QVariant


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/f49a0c3462176ccc34bf31dffbe6fd88d1baa0bd/qt__pyqt__pyside__pyqode/lazy__qtwidgets_itemviews_fetchmore_example__QAbstractListModel.py#L19
class FileListModel(QAbstractListModel):
    numberPopulated = pyqtSignal(int)

    def __init__(self, batch_size=50, parent=None):
        super().__init__(parent)

        self.fileList = []
        self.fileCount = 0
        self.batch_size = batch_size

    def rowCount(self, parent: QModelIndex = None) -> int:
        return self.fileCount

    def data(self, index: QModelIndex, role=Qt.DisplayRole) -> QVariant:
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self.fileList) or index.row() < 0:
            return QVariant()

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            return self.fileList[index.row()]

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

    def setFileList(self, fileList: list):
        self.beginResetModel()

        self.fileList = fileList
        self.fileCount = 0

        self.endResetModel()
