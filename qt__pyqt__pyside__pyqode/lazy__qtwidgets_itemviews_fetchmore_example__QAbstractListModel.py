#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://doc.qt.io/qt-5.12/qtwidgets-itemviews-fetchmore-example.html


from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QListView,
    QGridLayout,
    QLabel,
    QWidget,
    QLineEdit,
    QTextBrowser,
    QSizePolicy,
)
from PyQt5.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Qt,
    pyqtSignal,
    QVariant,
    QLibraryInfo,
)


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

        if role == Qt.DisplayRole:
            return self.fileList[index.row()]

        elif role == Qt.BackgroundRole:
            batch = (index.row() // self.batch_size) % 2
            if batch == 0:
                return QApplication.instance().palette().base()
            else:
                return QApplication.instance().palette().alternateBase()

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

    def setDirPath(self, path: str):
        self.beginResetModel()

        # Recursive
        self.fileList = [str(x.resolve()) for x in Path(path).rglob("*")]
        self.fileCount = 0

        self.endResetModel()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fetch More Example")

        label = QLabel("&Directory:")
        lineEdit = QLineEdit()
        label.setBuddy(lineEdit)

        self.model = FileListModel()
        self.model.numberPopulated.connect(self.updateLog)

        self.list_view = QListView()
        self.list_view.setModel(self.model)

        self.logViewer = QTextBrowser()
        self.logViewer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        lineEdit.textChanged.connect(self.model.setDirPath)
        lineEdit.textChanged.connect(self.logViewer.clear)

        lineEdit.setText(
            str(Path(QLibraryInfo.location(QLibraryInfo.PrefixPath)).resolve())
        )

        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(lineEdit, 0, 1)
        layout.addWidget(self.list_view, 1, 0, 1, 2)
        layout.addWidget(self.logViewer, 2, 0, 1, 2)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)

    def updateLog(self, number: int):
        self.logViewer.append(f"{number} items added.")


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.resize(800, 600)
    mw.show()

    app.exec()
