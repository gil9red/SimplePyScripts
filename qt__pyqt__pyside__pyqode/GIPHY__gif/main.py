#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/q/1134473/201445


import time
import sys
import traceback

import requests

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QMessageBox,
    QLineEdit,
    QPushButton,
    QLabel,
    QScrollArea,
    QWidget,
    QGridLayout,
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QMovie

from config import GIPHY_API_KEY, TEMP_DIR


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "{}: {}:\n".format(ex_cls.__name__, ex)
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class SearchGifThread(QThread):
    SITE_URL = "https://api.giphy.com/v1"

    about_add_gif = pyqtSignal(dict, int, int)

    def __init__(self, name_gif=None):
        super().__init__()

        self.name_gif = name_gif

    def get_gif(self) -> dict:
        url = f"{self.SITE_URL}/gifs/search?api_key={GIPHY_API_KEY}&q={self.name_gif}"

        try:
            rs = requests.get(url)
            rs.raise_for_status()

            data = rs.json()["data"]
            if data:
                return data

        except Exception as e:
            # TODO: emit error to MainWindow
            print(e)

        # TODO: emit 'not found' to MainWindow
        return {"error": True}

    def _process_gif(self, img: dict, index: int) -> dict:
        url_gif = img["images"]["fixed_width"]["url"]
        image_rs = requests.get(url_gif)
        image_rs.raise_for_status()

        file_name = TEMP_DIR / f"img{index}.gif"
        with open(file_name, "wb") as f:
            f.write(image_rs.content)

        data = {
            "row": index // 3,
            "col": index % 3,
            "error": None,
            "file_name": str(file_name),
        }
        return data

    def run(self):
        data = self.get_gif()
        if "error" in data:
            # TODO: emit error to MainWindow
            return

        for i, img in enumerate(data):
            data_gif = self._process_gif(img, i)
            self.about_add_gif.emit(data_gif, i + 1, len(data))

            time.sleep(1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Gif Manager"
        self.setWindowTitle(self.title)

        self.search_gif_thread = SearchGifThread()
        self.search_gif_thread.started.connect(self.on_start)
        self.search_gif_thread.finished.connect(self.on_finish)
        self.search_gif_thread.about_add_gif.connect(self.add_gif)

        self.init_ui()

    def init_ui(self):
        self.gif_edit = QLineEdit()
        self.gif_edit.returnPressed.connect(self.search_gif)
        self.gif_edit.setPlaceholderText("Enter name gif")

        gif_search_button = QPushButton("Search gif")
        gif_search_button.clicked.connect(self.search_gif)

        gif_data_layout = QHBoxLayout()
        gif_data_layout.setContentsMargins(0, 0, 0, 0)
        gif_data_layout.addWidget(self.gif_edit)
        gif_data_layout.addWidget(gif_search_button)

        self.gif_data_frame = QFrame()
        self.gif_data_frame.setLayout(gif_data_layout)

        self.info_label = QLabel(
            '<font color="red">Something went wrong. Check that the request was made correctly.</font>'
        )
        self.info_label.setAlignment(Qt.AlignHCenter)
        self.info_label.hide()

        scrollWidget = QWidget()
        self.gifs_layout = QGridLayout(scrollWidget)

        self.scroll = QScrollArea()
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(scrollWidget)

        root_widget = QWidget()
        self.setCentralWidget(root_widget)

        root_layout = QVBoxLayout(root_widget)
        root_layout.addWidget(self.gif_data_frame)
        root_layout.addWidget(self.info_label)
        root_layout.addWidget(self.scroll)

    def on_finish(self):
        self.gif_data_frame.setEnabled(True)

    def on_start(self):
        self.info_label.hide()
        self.scroll.show()
        self.gif_data_frame.setEnabled(False)

    def search_gif(self):
        # TODO: replace on QListWidget
        for i in range(self.gifs_layout.count()):
            self.gifs_layout.itemAt(i).widget().deleteLater()

        self.search_gif_thread.name_gif = self.gif_edit.text()
        self.search_gif_thread.start()

    def add_gif(self, data: dict, num: int, total: int):
        self.setWindowTitle(f"{self.title}. {num} / {total}")

        if data["error"]:
            self.gif_data_frame.setEnabled(True)
            self.scroll.hide()
            self.info_label.show()
            return

        row, col, error, file_name = data.values()
        movie = QMovie(file_name)
        movie.setSpeed(200)
        label_gif = QLabel()
        label_gif.setMovie(movie)
        movie.start()

        self.gifs_layout.addWidget(label_gif, row, col)
        label_gif.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.resize(800, 600)
    mw.show()

    mw.gif_edit.setText("cat")

    sys.exit(app.exec_())
