#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
import traceback
from urllib.request import urlretrieve

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QTextEdit,
)
from PyQt5.QtCore import QThread, pyqtSignal


class ThreadDownload(QThread):
    about_progress = pyqtSignal(str)
    about_file_name = pyqtSignal(str)
    about_error = pyqtSignal(str)

    def __init__(self, url: str = None, file_name: str = None) -> None:
        super().__init__()

        self.url = url
        self.file_name = file_name

    # SOURCE: https://github.com/gil9red/SimplePyScripts/blob/4692cbb36b5addb0f2bd5e93e69eb8c7c257bdf8/download_file/with_progress.py#L12
    def reporthook(self, blocknum, blocksize, totalsize) -> None:
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 100.0 / totalsize
            if percent > 100:
                percent = 100
                readsofar = totalsize

            s = "%5.1f%% %*d / %d" % (
                percent,
                len(str(totalsize)),
                readsofar,
                totalsize,
            )
            self.about_progress.emit(s)

        # Total size is unknown
        else:
            self.about_progress.emit(f"read {readsofar}")

    def run(self) -> None:
        try:
            file_name, _ = urlretrieve(
                self.url, self.file_name, reporthook=self.reporthook
            )
            file_name = os.path.abspath(file_name)
            self.about_file_name.emit(file_name)

        except:
            self.about_error.emit(traceback.format_exc())


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.line_edit_url = QLineEdit(
            "https://codeload.github.com/gil9red/SimplePyScripts/zip/master"
        )
        self.line_edit_file_name = QLineEdit("SimplePyScripts.zip")

        self.button_download = QPushButton("Download")
        self.button_download.clicked.connect(self.download)

        self.text_edit_log = QTextEdit()

        layout = QFormLayout()
        layout.addRow("URL:", self.line_edit_url)
        layout.addRow("File Name:", self.line_edit_file_name)
        layout.addWidget(self.button_download)
        layout.addWidget(self.text_edit_log)

        self.thread = ThreadDownload()
        self.thread.started.connect(lambda: self.button_download.setEnabled(False))
        self.thread.finished.connect(lambda: self.button_download.setEnabled(True))
        self.thread.about_progress.connect(self._handle_about_progress)
        self.thread.about_file_name.connect(self._handle_about_file_name)
        self.thread.about_error.connect(self._handle_about_error)

        self.setLayout(layout)

    def download(self) -> None:
        self.thread.url = self.line_edit_url.text()
        self.thread.file_name = self.line_edit_file_name.text()
        self.thread.start()

    def _handle_about_progress(self, text: str) -> None:
        self.setWindowTitle(text)

    def _handle_about_file_name(self, text: str) -> None:
        self.text_edit_log.append(
            f"""<b><p style="color:green">File name: {text}</p></b>"""
        )

    def _handle_about_error(self, text: str) -> None:
        self.text_edit_log.append(f"""<pre style="color:red">{text}</pre>""")


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
