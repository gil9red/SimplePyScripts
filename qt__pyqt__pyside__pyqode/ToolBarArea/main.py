#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class Widget(Qt.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("ToolBarArea")

        self.toolbar = self.addToolBar("Panel2")
        self.toolbar.addAction("1")
        self.toolbar.addAction("2")
        self.toolbar.addAction("3")

        self.toolbar2 = self.addToolBar("Panel1")
        self.addToolBar(Qt.Qt.LeftToolBarArea, self.toolbar2)
        self.toolbar2.addAction("a")
        self.toolbar2.addAction("b")
        self.toolbar2.addAction("c")

        self.toolbar3 = Qt.QToolBar("Panel3")
        self.addToolBar(Qt.Qt.RightToolBarArea, self.toolbar3)
        self.toolbar3.addAction("x")
        self.toolbar3.addAction("y")
        self.toolbar3.addAction("z")

        self.toolbar4 = Qt.QToolBar("Panel4")
        self.addToolBar(Qt.Qt.BottomToolBarArea, self.toolbar4)
        self.toolbar4.addAction("+")
        self.toolbar4.addAction("-")
        self.toolbar4.addAction("=")


if __name__ == "__main__":
    app = Qt.QApplication([])

    w = Widget()
    w.show()

    app.exec()
