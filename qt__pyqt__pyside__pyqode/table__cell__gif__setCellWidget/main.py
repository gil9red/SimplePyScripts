#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class Window(Qt.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.table = Qt.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(3)

        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                movie = Qt.QMovie("loading.gif")
                item = Qt.QLabel()
                item.setMovie(movie)
                movie.start()

                self.table.setCellWidget(i, j, item)

        main_layout = Qt.QHBoxLayout()
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = Window()
    mw.show()

    app.exec()
