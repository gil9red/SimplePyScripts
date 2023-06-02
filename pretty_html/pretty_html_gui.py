#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from os.path import split as path_split

try:
    from PyQt5.QtWidgets import (
        QWidget,
        QVBoxLayout,
        QPlainTextEdit,
        QLabel,
        QSizePolicy,
        QPushButton,
        QSplitter,
        QHBoxLayout,
        QMessageBox,
        QErrorMessage,
        QTextEdit,
        QApplication,
    )
    from PyQt5.QtCore import Qt

except:
    try:
        from PyQt4.QtGui import (
            QWidget,
            QVBoxLayout,
            QPlainTextEdit,
            QLabel,
            QSizePolicy,
            QPushButton,
            QSplitter,
            QHBoxLayout,
            QMessageBox,
            QErrorMessage,
            QTextEdit,
            QApplication,
        )
        from PyQt4.QtCore import Qt

    except:
        from PySide.QtGui import (
            QWidget,
            QVBoxLayout,
            QPlainTextEdit,
            QLabel,
            QSizePolicy,
            QPushButton,
            QSplitter,
            QHBoxLayout,
            QMessageBox,
            QErrorMessage,
            QTextEdit,
            QApplication,
        )
        from PySide.QtCore import Qt

from pretty_html import pretty_html


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(path_split(__file__)[1])

        layout = QVBoxLayout()

        self.text_edit_input = QPlainTextEdit()
        self.text_edit_output = QPlainTextEdit()

        self.label_error = QLabel()
        self.label_error.setStyleSheet("QLabel { color : red; }")
        self.label_error.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_error.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.button_detail_error = QPushButton("...")
        self.button_detail_error.setFixedSize(20, 20)
        self.button_detail_error.setToolTip("Detail error")
        self.button_detail_error.hide()

        self.last_error_message = None
        self.last_detail_error_message = None

        self.button_detail_error.clicked.connect(self.show_detail_error_message)
        self.text_edit_input.textChanged.connect(self.input_text_changed)

        splitter = QSplitter()
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        splitter.addWidget(self.text_edit_input)
        splitter.addWidget(self.text_edit_output)

        layout.addWidget(splitter)

        layout_error = QHBoxLayout()
        layout_error.addWidget(self.label_error)
        layout_error.addWidget(self.button_detail_error)

        layout.addLayout(layout_error)

        self.setLayout(layout)

    def input_text_changed(self):
        self.label_error.clear()
        self.button_detail_error.hide()

        self.last_error_message = None
        self.last_detail_error_message = None

        try:
            text = self.text_edit_input.toPlainText()
            text = pretty_html(text)
            self.text_edit_output.setPlainText(text)

        except Exception as e:
            # Выводим ошибку в консоль
            traceback.print_exc()

            # Сохраняем в переменную
            tb = traceback.format_exc()

            self.last_error_message = str(e)
            self.last_detail_error_message = str(tb)
            self.button_detail_error.show()

            self.label_error.setText("Error: " + self.last_error_message)

    def show_detail_error_message(self):
        message = self.last_error_message + "\n\n" + self.last_detail_error_message

        mb = QErrorMessage()
        mb.setWindowTitle("Error")
        # Сообщение ошибки содержит отступы, символы-переходы на следующую строку,
        # которые поломаются при вставке через QErrorMessage.showMessage, и нет возможности
        # выбрать тип текста, то делаем такой хак.
        mb.findChild(QTextEdit).setPlainText(message)

        mb.exec_()


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.resize(650, 500)
    mw.show()

    mw.text_edit_input.setPlainText(
        "<!DOCTYPE html><html><head><title>Example</title></head><body>"
        "<p>This is an example of a simple HTML page with one paragraph.</p>"
        "</body></html>"
    )

    app.exec_()
