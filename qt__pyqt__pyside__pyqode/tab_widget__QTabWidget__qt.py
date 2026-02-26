#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self._on_close_tab)

        tool_bar = self.addToolBar("General")
        self.action_add_tab = tool_bar.addAction("Add tab")
        self.action_add_tab.triggered.connect(self.add_tab)

        self.action_remove_tab = tool_bar.addAction("Remove tab")
        self.action_remove_tab.triggered.connect(self.remove_tab)

        self.setCentralWidget(self.tab_widget)

        self.update_states()

    def update_states(self) -> None:
        self.action_add_tab.setEnabled(self.tab_widget.count() < 3)
        self.action_remove_tab.setEnabled(self.tab_widget.count() > 0)

    def add_tab(self) -> None:
        tab = QTextEdit()
        self.tab_widget.addTab(tab, str(self.tab_widget.count() + 1))

        self.update_states()

    def remove_tab(self) -> None:
        index = self.tab_widget.currentIndex()
        self._on_close_tab(index)

    def _on_close_tab(self, index) -> None:
        if index == -1:
            return

        self.tab_widget.removeTab(index)

        self.update_states()


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
