#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class Window(Qt.QWidget):
    def __init__(self):
        super().__init__()

        self.table = Qt.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(3)

        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                icon = Qt.QIcon()
                icon.addFile("loading.gif")

                item = Qt.QTableWidgetItem()
                item.setIcon(icon)

                self.table.setItem(i, j, item)

        main_layout = Qt.QHBoxLayout()
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = Window()
    mw.show()

    app.exec()
