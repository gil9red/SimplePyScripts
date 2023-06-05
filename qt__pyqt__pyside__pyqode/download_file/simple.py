#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
import traceback

from threading import Thread
from urllib.request import urlretrieve

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFormLayout


def download_file(url: str, file_name: str):
    try:
        local_file_name, _ = urlretrieve(url, file_name)
        print(os.path.abspath(local_file_name))
    except:
        print(traceback.format_exc())


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.line_edit_url = QLineEdit(
            "https://codeload.github.com/gil9red/SimplePyScripts/zip/master"
        )
        self.line_edit_file_name = QLineEdit("SimplePyScripts.zip")

        self.button_download = QPushButton("Download")
        self.button_download.clicked.connect(self.download)

        layout = QFormLayout()
        layout.addRow("URL:", self.line_edit_url)
        layout.addRow("File Name:", self.line_edit_file_name)
        layout.addWidget(self.button_download)

        self.setLayout(layout)

    def download(self):
        url = self.line_edit_url.text()
        file_name = self.line_edit_file_name.text()

        thread = Thread(target=download_file, args=(url, file_name))
        thread.start()


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
