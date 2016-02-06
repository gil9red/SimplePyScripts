#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

from PySide.QtGui import *
from PySide.QtCore import *


if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = QStandardItemModel()
    header_labels = ['Имя', 'Размер']
    model.setColumnCount(len(header_labels))
    model.setHorizontalHeaderLabels(header_labels)

    for drive in QDir.drives():
        model.appendRow([QStandardItem(drive.path()), QStandardItem(drive.size())])

    tree = QTreeView()
    tree.setModel(model)

    # Demonstrating look and feel features
    tree.setAnimated(False)
    tree.setIndentation(20)
    tree.setSortingEnabled(True)

    tree.setWindowTitle("Dirs Sizes")
    tree.resize(640, 480)
    tree.show()

    sys.exit(app.exec_())
