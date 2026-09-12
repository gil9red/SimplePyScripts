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
    numberPopulated = pyqtSignal(int, int, int)

    IsMainRole: int = Qt.ItemDataRole.UserRole
    IsMatchedRole: int = Qt.ItemDataRole.UserRole + 1

    def __init__(self, batch_size: int = 50, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.batch_size: int = batch_size

        self.total_file_list: list[str] = []
        self.current_file_count: int = 0

        self.main_file: str | None = None
        self.matched_files: list[str] = []
        self.mark_matching: bool = True

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        return self.current_file_count

    @property
    def total_file_count(self) -> int:
        return len(self.total_file_list)

    def data(
        self,
        index: QModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> QVariant:
        if not index.isValid():
            return QVariant()

        if index.row() >= self.total_file_count or index.row() < 0:
            return QVariant()

        file_name = self.total_file_list[index.row()]

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
        return self.current_file_count < self.total_file_count

    def fetchMore(self, parent: QModelIndex | None = None) -> None:
        remainder: int = self.total_file_count - self.current_file_count
        items_to_fetch: int = min(self.batch_size, remainder)
        if items_to_fetch <= 0:
            return

        self.beginInsertRows(
            QModelIndex(),
            self.current_file_count,
            self.current_file_count + items_to_fetch - 1,
        )

        self.current_file_count += items_to_fetch

        self.endInsertRows()

        self.numberPopulated.emit(
            items_to_fetch, self.current_file_count, self.total_file_count
        )

    def set_total_file_list(self, file_list: list[str]) -> None:
        self.beginResetModel()

        self.total_file_list = file_list
        self.current_file_count = 0
        self.numberPopulated.emit(0, 0, 0)

        self.endResetModel()

    def set_matched_files(self, main_file: str, file_list: list[str]) -> None:
        self.main_file = main_file

        self.matched_files.clear()
        self.matched_files.extend(file_list)

    def set_mark_matching(self, mark_matching: bool) -> None:
        self.mark_matching = mark_matching

    def get_index_by_file_name(self, file_name: str, column: int = 0) -> QModelIndex:
        try:
            row = self.total_file_list.index(file_name)
            return self.index(row, column)
        except ValueError:
            pass

        return QModelIndex()
