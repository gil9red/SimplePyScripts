#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from string import printable
from typing import Iterator

from PyQt5.QtWidgets import QApplication, QWidget, QListView, QGroupBox, QHBoxLayout

from iterator_list_model import IteratorListModel


def get_infinity_generator():
    i = 0
    while True:
        yield i
        i += 1


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(
            self._add_view_with_it("infinity_generator", get_infinity_generator())
        )
        main_layout.addWidget(
            self._add_view_with_it("range(1_000_000)", range(1_000_000))
        )
        main_layout.addWidget(
            self._add_view_with_it("list of pow2", [str(i**i) for i in range(1_000)])
        )
        main_layout.addWidget(self._add_view_with_it("str", printable * 100))
        main_layout.addWidget(self._add_view_with_it("dict", dict.fromkeys(dir(self))))

    def _add_view_with_it(self, title: str, it: Iterator) -> QWidget:
        group_box = QGroupBox()
        group_box.setTitle("1111")

        model = IteratorListModel(it=it)
        model.rowsInserted.connect(
            lambda: group_box.setTitle(f"[{title}] rows: {model.rowCount()}")
        )

        view = QListView()
        view.setModel(model)

        layout = QHBoxLayout(group_box)
        layout.addWidget(view)

        return group_box


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
