#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QFrame


class HorizontalLineWidget(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(1)


class VerticalLineWidget(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(1)


if __name__ == "__main__":
    from PyQt5.QtWidgets import (
        QApplication,
        QFormLayout,
        QHBoxLayout,
        QLineEdit,
        QCheckBox,
        QWidget,
        QLabel,
    )
    from PyQt5.QtCore import Qt

    app = QApplication([])

    layout = QFormLayout()
    layout.addRow("First", QLineEdit())
    layout.addRow("Last", QLineEdit())
    layout.addRow(HorizontalLineWidget())

    layout.addRow("Phone", QLineEdit())
    layout.addRow(HorizontalLineWidget())

    h_layout = QHBoxLayout()
    label = QLabel("1")
    label.setAlignment(Qt.AlignCenter)
    h_layout.addWidget(label)
    h_layout.addWidget(VerticalLineWidget())

    label = QLabel("2")
    label.setAlignment(Qt.AlignCenter)
    h_layout.addWidget(label)
    h_layout.addWidget(VerticalLineWidget())

    label = QLabel("3")
    label.setAlignment(Qt.AlignCenter)
    h_layout.addWidget(label)

    layout.addItem(h_layout)

    layout.addRow("Ok?", QCheckBox())

    mw = QWidget()
    mw.setLayout(layout)
    mw.show()

    app.exec()
