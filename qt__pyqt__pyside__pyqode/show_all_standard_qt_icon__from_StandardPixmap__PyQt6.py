#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from PyQt6.QtWidgets import (
    QApplication,
    QMessageBox,
    QGridLayout,
    QPushButton,
    QStyle,
    QWidget,
    QToolTip,
)
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import QRect


# Для отлова всех исключений, которые в слотах Qt могут "затеряться" и привести к тихому падению
def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print("Error: ", text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


if __name__ == "__main__":
    app = QApplication([])
    style = app.style()

    source = QStyle.StandardPixmap

    enum_items_standard_pixmap: list[str] = [x for x in dir(source) if x.startswith("SP_")]

    mw = QWidget()
    mw.setWindowTitle("show_all_standard_qt_icon__from_StandardPixmap__PyQt6")

    layout = QGridLayout()

    max_column: int = 4
    for i, enum_name in enumerate(enum_items_standard_pixmap):
        enum_value = getattr(source, enum_name)
        icon = style.standardIcon(enum_value)

        button = QPushButton(icon, enum_name)
        button.clicked.connect(
            lambda checked, w=button: (
                app.clipboard().setText(w.text()),
                QToolTip.showText(
                    QCursor.pos(),
                    "Saved to clipboard",
                    w,
                    QRect(),
                    2000,
                ),
            )
        )

        row = i // max_column
        col = i % max_column
        layout.addWidget(button, row, col)

    mw.setLayout(layout)
    mw.show()

    app.exec()
