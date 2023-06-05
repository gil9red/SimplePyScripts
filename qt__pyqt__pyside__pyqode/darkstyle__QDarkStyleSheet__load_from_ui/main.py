#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt
from PyQt5 import uic

# pip install qdarkstyle
import qdarkstyle


class MainWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("mainwidget.ui", self)

        self.cbPenStyle.addItem("Solid", Qt.Qt.SolidLine)
        self.cbPenStyle.addItem("Dash", Qt.Qt.DashLine)
        self.cbPenStyle.addItem("Dot", Qt.Qt.DotLine)
        self.cbPenStyle.addItem("Dash Dot", Qt.Qt.DashDotLine)
        self.cbPenStyle.addItem("Dash Dot Dot", Qt.Qt.DashDotDotLine)

        self.pen_color = Qt.Qt.green

        self.pbPenColor.clicked.connect(self._choose_color)
        self.pbPenColor.setIconSize(self.pbPenColor.size())

        self._update_pen_color()

    def _choose_color(self):
        color = Qt.QColorDialog.getColor(self.pen_color)
        if not color.isValid():
            return

        self.pen_color = color
        self._update_pen_color()

    def _update_pen_color(self):
        pixmap = Qt.QPixmap(self.pbPenColor.size())
        pixmap.fill(self.pen_color)
        self.pbPenColor.setIcon(Qt.QIcon(pixmap))


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw1 = MainWindow()
    mw1.setWindowTitle("Standard")
    mw1.show()

    mw2 = MainWindow()
    mw2.setWindowTitle("Dark")
    mw2.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mw2.show()

    app.exec_()
