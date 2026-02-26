#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTranslator, QLibraryInfo


def question() -> None:
    QMessageBox.question(
        None,
        "TITLE",
        "TEXT",
        QMessageBox.Yes | QMessageBox.No | QMessageBox.Abort,
    )


app = QApplication([])

# NOTE: EN
question()

translator = QTranslator()
if translator.load("qtbase_ru", directory=QLibraryInfo.location(QLibraryInfo.TranslationsPath)):
    app.installTranslator(translator)

# NOTE: RU
question()
