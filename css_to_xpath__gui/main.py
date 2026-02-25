#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys

from PyQt5 import Qt

# pip install cssselect
from cssselect import HTMLTranslator


css_to_xpath = HTMLTranslator(xhtml=True).css_to_xpath


def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class MainWindow(Qt.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("css_to_xpath__gui")

        self.text_edit_input = Qt.QPlainTextEdit()
        self.text_edit_output = Qt.QPlainTextEdit()

        self.label_error = Qt.QLabel()
        self.label_error.setStyleSheet("QLabel { color : red; }")
        self.label_error.setTextInteractionFlags(Qt.Qt.TextSelectableByMouse)
        self.label_error.setSizePolicy(
            Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Preferred
        )

        self.button_detail_error = Qt.QPushButton("...")
        self.button_detail_error.setFixedSize(20, 20)
        self.button_detail_error.setToolTip("Detail error")
        self.button_detail_error.hide()

        self.last_error_message = None
        self.last_detail_error_message = None

        self.text_edit_input.textChanged.connect(self.on_process)
        self.button_detail_error.clicked.connect(self.show_detail_error_message)

        splitter = Qt.QSplitter()
        splitter.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
        splitter.addWidget(self.text_edit_input)
        splitter.addWidget(self.text_edit_output)

        layout = Qt.QVBoxLayout()
        layout.addWidget(splitter)

        layout_error = Qt.QHBoxLayout()
        layout_error.addWidget(self.label_error)
        layout_error.addWidget(self.button_detail_error)

        layout.addLayout(layout_error)

        self.setLayout(layout)

    def on_process(self) -> None:
        self.text_edit_output.clear()
        self.label_error.clear()
        self.button_detail_error.hide()

        self.last_error_message = None
        self.last_detail_error_message = None

        try:
            text = self.text_edit_input.toPlainText()
            if not text.strip():
                return

            output = css_to_xpath(text)
            self.text_edit_output.setPlainText(output)

        except Exception as e:
            # # Выводим ошибку в консоль
            # traceback.print_exc()

            # Сохраняем в переменную
            tb = traceback.format_exc()

            self.last_error_message = str(e)
            self.last_detail_error_message = str(tb)
            self.button_detail_error.show()

            self.label_error.setText("Error: " + self.last_error_message)

    def show_detail_error_message(self) -> None:
        message = self.last_error_message + "\n\n" + self.last_detail_error_message

        mb = Qt.QErrorMessage()
        mb.setWindowTitle("Error")
        # Сообщение ошибки содержит отступы, символы-переходы на следующую строку,
        # которые поломаются при вставке через QErrorMessage.showMessage, и нет возможности
        # выбрать тип текста, то делаем такой хак.
        mb.findChild(Qt.QTextEdit).setPlainText(message)

        mb.exec_()


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.resize(400, 300)
    mw.show()

    # For example
    mw.text_edit_input.setPlainText("div#main > a[href]")

    app.exec_()
