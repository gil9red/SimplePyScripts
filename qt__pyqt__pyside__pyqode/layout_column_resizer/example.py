#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import platform

from datetime import datetime
from pathlib import Path

from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QFormLayout,
    QLabel,
    QDialogButtonBox,
    QGroupBox,
    QVBoxLayout,
    QScrollArea,
)

from column_resizer import ColumnResizer


DIR: Path = Path(__file__).resolve().parent

PROGRAM_NAME: str = DIR.name


class About(QDialog):
    def __init__(self, title: str, use_column_resizer: bool):
        super().__init__()

        self.setWindowTitle(title)

        self._started: datetime = datetime.now()

        gb_python = QGroupBox("Python:")
        gb_python_layout = QFormLayout(gb_python)
        gb_python_layout.addRow(
            "Version:",
            QLabel(sys.version),
        )
        gb_python_layout.addRow(
            "Implementation:",
            QLabel(platform.python_implementation()),
        )
        gb_python_layout.addRow("Executable:", QLabel(sys.executable))

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        fields_layout = QFormLayout()
        fields_layout.addRow(
            "Version:",
            QLabel("1.0.0"),
        )
        fields_layout.addRow(
            "Directory:",
            QLabel(str(DIR)),
        )
        fields_layout.addRow(
            "Argv:",
            QLabel(" ".join(sys.argv[1:])),
        )
        fields_layout.addRow(gb_python)
        fields_layout.addRow(
            "Platform:",
            QLabel(platform.platform()),
        )

        fields_widget = QWidget()
        fields_layout.setContentsMargins(0, 0, 0, 0)
        fields_widget.setLayout(fields_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(fields_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QScrollArea.NoFrame)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel(f"<h1>{PROGRAM_NAME}</h1>"))
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(button_box)

        if use_column_resizer:
            resizer = ColumnResizer(self)
            resizer.addWidgetsFromLayout(fields_layout, 0)
            resizer.addWidgetsFromLayout(gb_python_layout, 0)

        self.resize(500, 300)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    w1 = About(f"use_column_resizer=False", use_column_resizer=False)
    w1.show()

    w2 = About(f"use_column_resizer=True", use_column_resizer=True)
    w2.show()
    w2.move(w1.x() + w1.width(), w1.y())

    sys.exit(app.exec())
