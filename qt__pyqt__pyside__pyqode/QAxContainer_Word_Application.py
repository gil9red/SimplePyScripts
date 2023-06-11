#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QApplication,
)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Document Word.Application")
        self.axWidget = QAxWidget(self)

        self.buttonOpen = QPushButton("Open")
        self.buttonOpen.clicked.connect(self.handleOpen)

        layout = QGridLayout(self)
        layout.addWidget(self.axWidget)
        layout.addWidget(self.buttonOpen)

    def handleOpen(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл word", "", "word(*.docx *.doc)"
        )
        if not path:
            return

        return self.openOffice(path, "Word.Application")

    def openOffice(self, path, app):
        self.axWidget.clear()
        if not self.axWidget.setControl(app):
            return QMessageBox.critical(self, "Ошибка", f"Нет установки {app!r}")

        self.axWidget.dynamicCall("SetVisible (bool Visible)", "false")
        self.axWidget.setProperty("DisplayAlerts", False)
        self.axWidget.setControl(path)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = Window()
    mw.resize(840, 480)
    mw.show()

    sys.exit(app.exec())
