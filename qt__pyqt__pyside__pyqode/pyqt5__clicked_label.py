#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import QLabel, pyqtSignal, QApplication, QVBoxLayout, QWidget


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)

        self.clicked.emit()


if __name__ == "__main__":
    app = QApplication([])

    label_1 = ClickedLabel("Label 1")
    label_1.clicked.connect(lambda: print("label_1"))

    label_2 = ClickedLabel("Label 2")
    label_2.clicked.connect(lambda: print("label_2"))

    layout = QVBoxLayout()
    layout.addWidget(label_1)
    layout.addWidget(label_2)

    mw = QWidget()
    mw.setLayout(layout)
    mw.show()

    app.exec()
