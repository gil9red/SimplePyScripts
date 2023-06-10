#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore


class MessagesWindow(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setModel(ModelMessages())
        self.setItemDelegateForColumn(0, ItemDateFormat())
        self.setShowGrid(True)


class ModelMessages(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.appendRow(
            [
                QtGui.QStandardItem("2018-11-25 11:15:06.0001"),
                QtGui.QStandardItem("111"),
            ]
        )
        self.appendRow(
            [
                QtGui.QStandardItem("2018-11-25 11:15:06.0001"),
                QtGui.QStandardItem("111"),
            ]
        )
        self.appendRow(
            [
                QtGui.QStandardItem("2018-11-25 11:15:06.0001"),
                QtGui.QStandardItem("111"),
            ]
        )


class ItemDateFormat(QtWidgets.QItemDelegate):
    def paint(self, painter, opt: QtWidgets.QStyleOptionViewItem, index):
        self.drawBackground(painter, opt, index)
        self.drawFocus(painter, opt, opt.rect)
        try:
            opt.text = "{0:%d %b %H:%M}".format(
                datetime.strptime(index.model().data(index), "%Y-%m-%d %H:%M:%S.%f")
            )
        except TypeError:
            pass

        opt.font.setItalic(True)
        opt.backgroundBrush = QtCore.Qt.yellow

        QtWidgets.QApplication.style().drawControl(
            QtWidgets.QStyle.CE_ItemViewItem, opt, painter
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    w = MessagesWindow()
    w.show()

    app.exec()
