#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Пример реализации алгоритма выделения предыдущей вкладки.

"""


from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.prev_tab_index = -1
        self.curr_tab_index = 0

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(QLabel("1"), "1")
        self.tab_widget.addTab(QLabel("2"), "2")
        self.tab_widget.addTab(QLabel("3"), "3")
        self.tab_widget.addTab(QLabel("4"), "4")
        self.tab_widget.addTab(QLabel("5"), "5")
        self.tab_widget.setCurrentIndex(self.curr_tab_index)

        self.tab_widget.currentChanged.connect(self.current_tab_changed)

        self.setCentralWidget(self.tab_widget)

    def current_tab_changed(self, i) -> None:
        # Запоминание индексов предыдущей и текущей вкладки.
        # При переключении вкладок:
        #   У предыдущей убирается выделение
        #   Текущий индекс становится предыдущей
        #   У новой предыдущей добавляется выделение

        if self.prev_tab_index != -1:
            prev_text = self.tab_widget.tabText(self.prev_tab_index)
            self.tab_widget.setTabText(self.prev_tab_index, prev_text[1:-1])

        self.prev_tab_index = self.curr_tab_index
        prev_text = self.tab_widget.tabText(self.prev_tab_index)
        self.tab_widget.setTabText(self.prev_tab_index, "_" + prev_text + "_")

        self.curr_tab_index = i


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
