#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication
from PyQt5.QtCore import QDir


if __name__ == "__main__":
    app = QApplication([])

    model = QFileSystemModel()
    model.setRootPath(QDir.currentPath())
    model.setReadOnly(False)

    mw = QTreeView()
    mw.setModel(model)
    mw.setRootIndex(model.index(QDir.currentPath()))
    mw.show()

    app.exec()
