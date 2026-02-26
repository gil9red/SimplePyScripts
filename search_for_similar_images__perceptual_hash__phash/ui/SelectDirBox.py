#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/gil9red/VideoStreamingWithEncryption/blob/37cf7f501460a286ec44a20db7b2403e8cb05d97/server_GUI_Qt/inner_libs/gui/SelectDirBox.py


import os

from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QStyle,
)
from PyQt5.QtCore import pyqtSignal


class SelectDirBox(QWidget):
    valueChanged = pyqtSignal(str)
    valueEdited = pyqtSignal(str)

    def __init__(self, value="", visible_label=True) -> None:
        super().__init__()

        self._label = QLabel("Directory:")
        self._label.setVisible(visible_label)

        self._value = QLineEdit()
        self._value.textChanged.connect(self.valueChanged.emit)
        self._value.textEdited.connect(self.valueEdited.emit)

        icon_open_dir = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        action_open_dir = self._value.addAction(
            icon_open_dir, QLineEdit.TrailingPosition
        )
        action_open_dir.setToolTip("Open directory")
        action_open_dir.triggered.connect(self._on_open_dir)

        self._button_select_path = QPushButton("...")
        self._button_select_path.setFixedWidth(24)
        self._button_select_path.setToolTip("Select directory")
        self._button_select_path.clicked.connect(self._on_select_path)

        self.setValue(value)

        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._label)
        layout.addWidget(self._value, stretch=1)
        layout.addWidget(self._button_select_path)

        self.setLayout(layout)

    def setValue(self, value: str) -> None:
        self._value.setText(value)
        self._value.setToolTip(value)

    def getValue(self) -> str:
        return self._value.text()

    def _on_select_path(self) -> None:
        path = QFileDialog.getExistingDirectory(self, None, self._value.text())
        if not path:
            return

        self.setValue(path)

    def _on_open_dir(self) -> None:
        path = self._value.text()
        if os.path.isdir(path):
            os.startfile(path)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

        self._button_select_path.setFixedHeight(self._value.height())


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])

    mw = SelectDirBox()
    mw.valueChanged.connect(lambda value: print(f"Selected directory: {value}"))
    mw.show()

    app.exec()
