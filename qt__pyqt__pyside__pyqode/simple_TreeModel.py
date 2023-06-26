#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from typing import Union, Optional

from PyQt5.QtWidgets import QApplication, QTreeView, QMessageBox
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class TreeItem:
    def __init__(self, *args):
        self._childItems: list[TreeItem] = []
        self._itemData = args
        self._parentItem: TreeItem = None
        self._model: QAbstractItemModel = None

    def appendChild(self, child: Union["TreeItem", str]) -> "TreeItem":
        if isinstance(child, str):
            child = TreeItem(child)

        if self._model:
            self._model.beginInsertRows(
                self.index(), self.childCount(), self.childCount() + 1
            )

        child._parentItem = self
        child._model = self._model
        self._childItems.append(child)

        if self._model:
            self._model.endInsertRows()

        return child

    def appendChilds(self, childs: list["TreeItem"]):
        for x in childs:
            self.appendChild(x)

    def clearChilren(self):
        if self._model:
            self._model.beginRemoveRows(self.index(), 0, self.childCount())

        self._childItems.clear()

        if self._model:
            self._model.endRemoveRows()

    def child(self, row: int) -> Optional["TreeItem"]:
        if row < 0 or row >= len(self._childItems):
            return

        return self._childItems[row]

    def childCount(self) -> int:
        return len(self._childItems)

    def data(self, column: int):
        return self._itemData[column]

    def columnCount(self) -> int:
        return len(self._itemData)

    def row(self) -> int:
        if self._parentItem:
            return self._parentItem._childItems.index(self)
        return 0

    def parentItem(self) -> Optional["TreeItem"]:
        return self._parentItem

    def setModel(self, model: QAbstractItemModel):
        self._model = model

    def model(self) -> QAbstractItemModel:
        return self._model

    def index(self, column=0) -> QModelIndex:
        if self._parentItem is None:
            return QModelIndex()

        return self._model.createIndex(self.row(), column, self)


class TreeModel(QAbstractItemModel):
    column_names = ["File name"]

    def __init__(self):
        super().__init__()

        self._root_item = TreeItem("<ROOT>")
        self._root_item.setModel(self)

    def rootItem(self) -> TreeItem:
        return self._root_item

    def setModelData(self, items: list[TreeItem]):
        self.beginResetModel()

        self._root_item.clearChilren()
        self._root_item.appendChilds(items)

        self.endResetModel()

    def item(self, index: QModelIndex) -> TreeItem:
        if not index.isValid():
            return self._root_item

        return index.internalPointer()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.column_names)

    def rowCount(self, parent_index: QModelIndex = ...) -> int:
        item = self.item(parent_index)
        return item.childCount()

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        parentItem = self.item(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)

        return QModelIndex()

    def parent(self, child_index: QModelIndex) -> QModelIndex:
        if not child_index.isValid():
            return QModelIndex()

        childItem = child_index.internalPointer()
        parentItem = childItem.parentItem()
        if parentItem == self._root_item:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def headerData(self, section: int, orientation=Qt.Horizontal, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.column_names[section]
        return

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return

        item = index.internalPointer()

        if role == Qt.DisplayRole:
            return item.data(index.column())

        return


if __name__ == "__main__":
    from timeit import default_timer

    app = QApplication(sys.argv)

    t = default_timer()
    items = []
    for i in range(9999):
        item = TreeItem(f"root_{i:04}")
        items.append(item)

        for j in range(10):
            child = item.appendChild(f"item__{i:04}/{j}")

            for k in range(10):
                child.appendChild(f"item__{i:04}/{j}/{k}")
    print(f"Elapsed time: {default_timer() - t:.2f} secs")

    model = TreeModel()
    model.setModelData(items)

    view = QTreeView()
    view.setWindowTitle("Simple Tree Model")
    view.setAlternatingRowColors(True)
    view.setUniformRowHeights(True)  # Allows for scrolling optimizations.
    view.setModel(model)
    view.show()

    sys.exit(app.exec_())
