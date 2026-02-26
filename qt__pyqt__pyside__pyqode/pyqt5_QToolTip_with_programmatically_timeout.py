#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import QRect, QTimer


def show_tooltip(parent, widget) -> None:
    qtw.QToolTip.showText(
        parent.mapToGlobal(widget.pos()), widget.toolTip(), widget, QRect()
    )


if __name__ == "__main__":
    app = qtw.QApplication([])

    line_edit = qtw.QLineEdit()
    line_edit.setToolTip("This <b>my</b> LINE EDIT!")

    button = qtw.QPushButton("My button!")
    button.setToolTip("Simple button...")

    text_edit = qtw.QTextEdit()
    text_edit.setToolTip("TextEdit!")

    layout = qtw.QFormLayout()
    layout.addRow("Line edit:", line_edit)
    layout.addRow("Button:", button)
    layout.addRow("Text edit:", text_edit)

    w = qtw.QWidget()
    w.setWindowTitle("Tooltip example")
    w.setLayout(layout)
    w.show()

    QTimer.singleShot(1000, lambda: show_tooltip(w, line_edit))
    QTimer.singleShot(2000, lambda: show_tooltip(w, button))
    QTimer.singleShot(3000, lambda: show_tooltip(w, text_edit))

    app.exec()
