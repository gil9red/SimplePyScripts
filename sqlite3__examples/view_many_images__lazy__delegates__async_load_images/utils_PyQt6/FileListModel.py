#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt6.QtCore import (
    QObject,
    QAbstractListModel,
    QModelIndex,
    Qt,
    pyqtSignal,
    QVariant,
)


class FileListModel(QAbstractListModel):
    numberPopulated = pyqtSignal(int)

    IsMainRole: int = Qt.ItemDataRole.UserRole
    IsMatchedRole: int = Qt.ItemDataRole.UserRole + 1

    def __init__(self, batch_size: int = 50, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.batch_size: int = batch_size

        self.fileList: list[str] = []
        self.fileCount: int = 0

        self.main_file: str | None = None
        self.matched_files: list[str] = []
        self.mark_matching: bool = True

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        return self.fileCount

    def data(
        self,
        index: QModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> QVariant:
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self.fileList) or index.row() < 0:
            return QVariant()

        file_name = self.fileList[index.row()]

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.ToolTipRole:
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

    def canFetchMore(self, parent: QModelIndex | None = None) -> bool:
        return self.fileCount < len(self.fileList)

    def fetchMore(self, parent: QModelIndex | None = None) -> None:
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

    def set_file_list(self, file_list: list[str]) -> None:
        self.beginResetModel()

        self.fileList = file_list
        self.fileCount = 0

        self.endResetModel()

    def set_matched_files(self, main_file: str, file_list: list[str]) -> None:
        self.main_file = main_file

        self.matched_files.clear()
        self.matched_files.extend(file_list)

    def set_mark_matching(self, mark_matching: bool) -> None:
        self.mark_matching = mark_matching

    def get_index_by_file_name(self, file_name: str, column: int = 0) -> QModelIndex:
        try:
            row = self.fileList.index(file_name)
            return self.index(row, column)
        except ValueError:
            pass

        return QModelIndex()
