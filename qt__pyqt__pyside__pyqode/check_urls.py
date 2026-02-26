#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys

import requests

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QPlainTextEdit,
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt


def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit()


sys.excepthook = log_uncaught_exceptions


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"


class CheckUrlThread(QThread):
    about_check_url = pyqtSignal(str, str)

    def __init__(self, urls: list[str] = None) -> None:
        super().__init__()

        self.urls = urls if urls else []

    def run(self) -> None:
        for url in self.urls:
            try:
                rs = session.get(url)
                code = rs.status_code

            except Exception as e:
                # Пусть будет исключение
                code = e

            code = str(code)

            self.about_check_url.emit(url, code)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.urls = QPlainTextEdit()

        headers = ["URL", "CODE"]

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(len(headers))
        self.result_table.setHorizontalHeaderLabels(headers)
        self.result_table.setAlternatingRowColors(True)
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.horizontalHeader().resizeSection(0, 200)

        self.pb_check = QPushButton("Check")
        self.pb_check.clicked.connect(self._on_click_check)

        layout = QHBoxLayout()
        layout.addWidget(self.urls)
        layout.addWidget(self.result_table)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.pb_check)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.thread = CheckUrlThread()
        self.thread.about_check_url.connect(self._on_about_check_url)
        self.thread.started.connect(lambda: self.pb_check.setEnabled(False))
        self.thread.finished.connect(lambda: self.pb_check.setEnabled(True))

    def _on_click_check(self) -> None:
        urls = self.urls.toPlainText().strip().splitlines()

        self.result_table.clearContents()
        self.result_table.setRowCount(0)

        for url in urls:
            row = self.result_table.rowCount()
            self.result_table.setRowCount(row + 1)

            self.result_table.setItem(row, 0, QTableWidgetItem(url))
            self.result_table.setItem(row, 1, QTableWidgetItem())

        self.thread.urls = urls
        self.thread.start()

    def _on_about_check_url(self, url: str, code: str) -> None:
        for item in self.result_table.findItems(url, Qt.MatchCaseSensitive):
            row = item.row()
            self.result_table.item(row, 1).setText(code)


if __name__ == "__main__":
    app = QApplication([])

    text = "\n".join(
        [
            "https://ru.stackoverflow.com",
            "https://ru.stackoverflow.com/questions/893436/",
            "https://google.com",
            "http://ya.ru",
            "http://not_found_site.123",
        ]
    )

    mw = MainWindow()
    mw.urls.setPlainText(text)
    mw.resize(800, 600)
    mw.show()

    app.exec()
