#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Iterator

from PyQt5.QtWidgets import QApplication, QListView
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant


class IteratorListModel(QAbstractListModel):
    def __init__(self, it: Iterator, prefetch=100, parent=None):
        super().__init__(parent)

        self._at_end = False
        self._it = iter(it)
        self._items = []
        self._prefetch = prefetch

    def canFetchMore(self, parent: QModelIndex = None) -> bool:
        return not self._at_end

    def fetchMore(self, parent: QModelIndex = None):
        if self._at_end:
            return

        old_rows = len(self._items)
        for _ in range(self._prefetch):
            try:
                value = next(self._it)
                self._items.append(value)

            # Если данные закончились
            except StopIteration:
                self._at_end = True
                break

        new_rows = len(self._items)
        if old_rows != new_rows:
            self.beginInsertRows(QModelIndex(), old_rows, new_rows)
            self.endInsertRows()

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> QVariant:
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self._items) or index.row() < 0:
            return QVariant()

        if role == Qt.DisplayRole:
            return self._items[index.row()]

        return QVariant()

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self._items)


if __name__ == '__main__':
    app = QApplication([])

    model = IteratorListModel(it=range(1_000_000))
    model.rowsInserted.connect(lambda: mw.setWindowTitle(f'Rows: {model.rowCount()}'))

    mw = QListView()
    mw.setModel(model)
    mw.show()

    app.exec()
