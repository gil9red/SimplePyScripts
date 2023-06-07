#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import sys
import traceback

from difflib import get_close_matches
from PyQt5.Qt import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QLineEdit,
)


# Для отлова исключений
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "{}: {}:\n".format(ex_cls.__name__, ex)
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.data = json.load(open("data.json", encoding="utf-8"))

        self.input_word = QLineEdit()
        self.output_te = QTextEdit()

        self.result_pb = QPushButton("Проверить!")
        self.result_pb.clicked.connect(self._check)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_word)
        main_layout.addWidget(self.result_pb)
        main_layout.addWidget(self.output_te)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def _check(self):
        word_user = self.input_word.text()
        output = self._retrive_definition(word_user)

        if type(output) == list:
            output = "\n".join(" - " + x for x in output)
        else:
            output = " - " + output

        self.output_te.setPlainText(output)

    def _retrive_definition(self, word):
        word = word.lower()

        if word in self.data:
            return self.data[word]
        elif word.title() in self.data:
            return self.data[word.title()]
        elif word.upper() in self.data:
            return self.data[word.upper()]
        else:
            items = get_close_matches(word, self.data.keys())
            if items:
                text = 'Может быть Вы имели в виду "{}"?'.format(items[0])
                ok = QMessageBox.question(self, "Вопрос", text)
                if ok == QMessageBox.Yes:
                    return self.data[items[0]]

        return "Слово пока не существует в словаре."


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
