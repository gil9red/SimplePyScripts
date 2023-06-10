#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from PyQt5.Qt import (
    QApplication,
    QMainWindow,
    QSplitter,
    QTreeView,
    QTextEdit,
    QFileSystemModel,
    QDir,
)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Direct tree")

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(os.getcwd()))
        self.tree.doubleClicked.connect(self._on_double_clicked)
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        splitter = QSplitter()
        splitter.addWidget(self.tree)
        splitter.addWidget(self.textEdit)
        splitter.setSizes([50, 200])

        self.setCentralWidget(splitter)

    def _on_double_clicked(self, index):
        file_name = self.model.filePath(index)

        with open(file_name, encoding="utf-8") as f:
            text = f.read()
            self.textEdit.setPlainText(text)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.resize(600, 400)
    mw.show()

    app.exec()
