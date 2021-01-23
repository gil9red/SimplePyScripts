#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import (
    QWidget, QFileSystemModel, QTreeView, QListWidget, QPushButton, QSplitter,
    QVBoxLayout, QApplication
)
from PyQt5.QtCore import QDir, Qt


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        path = QDir.rootPath()

        self.model = QFileSystemModel()
        self.model.setRootPath(path)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setSelectionMode(QTreeView.ExtendedSelection)
        self.tree_view.selectionModel().selectionChanged.connect(self._on_selection_changed)

        self.list_files = QListWidget()

        self.button_add = QPushButton('Добавить!')
        self.button_add.setEnabled(False)
        self.button_add.clicked.connect(self._on_add)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.list_files)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(splitter)
        main_layout.addWidget(self.button_add)

    def _on_selection_changed(self, selected, deselected):
        has = self.tree_view.selectionModel().hasSelection()
        self.button_add.setEnabled(has)

    def _on_add(self):
        for row in self.tree_view.selectionModel().selectedRows():
            path = self.model.filePath(row)
            self.list_files.addItem(path)


if __name__ == '__main__':
    app = QApplication([])

    w = Widget()
    w.show()

    app.exec()
