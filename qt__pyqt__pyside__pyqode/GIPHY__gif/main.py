#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://ru.stackoverflow.com/q/1134473/201445


import json
import time
import sys
from pathlib import Path

import requests

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox,
    QLineEdit, QPushButton, QLabel, QScrollArea, QWidget, QGridLayout
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QMovie

from config import GIPHY_API_KEY

# Absolute file name
TEMP_DIR = Path(__file__).resolve().parent / 'temp'
TEMP_DIR.mkdir(exist_ok=True)


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class SearchGifThread(QThread):
    SITE_URL = 'https://api.giphy.com/v1'

    about_add_gif = pyqtSignal(dict)

    def __init__(self, name_gif=None):
        super().__init__()

        self.name_gif = name_gif

    def get_gif(self) -> dict:
        url = f'{SearchGifThread.SITE_URL}/gifs/search?api_key={GIPHY_API_KEY}&q={self.name_gif}'

        try:
            rs = requests.get(url)
            rs.raise_for_status()

            data = json.loads(rs.content.decode('utf-8'))['data']
            if not data:
                # TODO: emit 'not found' to MainWindow
                data = {'error': 1}
                return data

            return data

        except Exception as err:
            # TODO: emit error to MainWindow
            print(err)

        return {'error': 1}

    def _process_gif(self, data: dict, index: int) -> dict:
        url_gif = data[index]['images']['fixed_width']['url']
        image_rs = requests.get(url_gif)
        image_rs.raise_for_status()

        file_name = TEMP_DIR / f"img{index}.gif"
        with open(file_name, 'wb') as f:
            f.write(image_rs.content)

        data = {'row': index // 3, 'col': index % 3, 'error': None, 'file_name': str(file_name)}
        return data

    def run(self):
        data = self.get_gif()
        if 'error' in data:
            # TODO: emit error to MainWindow
            return

        for i in range(20):
            data_gif = self._process_gif(data, i)
            self.about_add_gif.emit(data_gif)

            time.sleep(1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width = self.size().width()
        self.height = self.size().height()
        self.left = 200
        self.top = 300
        self.title = 'Gif Manager'

        self.search_gif_thread = SearchGifThread()
        self.search_gif_thread.started.connect(self.on_start)
        self.search_gif_thread.finished.connect(self.on_finish)
        self.search_gif_thread.about_add_gif.connect(self.add_gif)

        self.init_window()
        self.init_ui()

        self.gif_edit.setText('cat')

    def init_window(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

    def init_ui(self):
        root_layout = QVBoxLayout()
        gif_data_layout = QHBoxLayout()
        gif_data_layout.setAlignment(Qt.AlignTop)
        self.gif_data_frame = QFrame()

        self.gif_edit = QLineEdit()
        self.gif_edit.returnPressed.connect(self.search_gif)
        self.gif_edit.setPlaceholderText('Enter name gif')

        gif_search_button = QPushButton('Search gif')
        gif_search_button.clicked.connect(self.search_gif)
        gif_data_layout.addWidget(self.gif_edit)
        gif_data_layout.addWidget(gif_search_button)
        self.gif_data_frame.setLayout(gif_data_layout)
        root_layout.addWidget(self.gif_data_frame)
        self.info_label = QLabel('Something went wrong. Check that the request was made correctly.')
        self.info_label.setAlignment(Qt.AlignHCenter)
        self.info_label.hide()
        root_layout.addWidget(self.info_label)
        self.scroll = QScrollArea()
        self.scroll.setStyleSheet('background: rgba(255, 255, 255, 30%);')
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        scrollWidget = QWidget()
        self.gifs_layout = QGridLayout()
        scrollWidget.setLayout(self.gifs_layout)
        self.scroll.setWidget(scrollWidget)
        root_layout.addWidget(self.scroll)
        root_widget = QWidget()
        root_widget.setLayout(root_layout)
        self.setCentralWidget(root_widget)

    def on_finish(self):
        self.gif_data_frame.show()

    def on_start(self):
        self.info_label.hide()
        self.scroll.show()
        self.gif_data_frame.hide()

    def search_gif(self):
        # TODO: replace on QListWidget
        for i in range(self.gifs_layout.count()):
            self.gifs_layout.itemAt(i).widget().deleteLater()

        self.search_gif_thread.name_gif = self.gif_edit.text()
        self.search_gif_thread.start()

    def add_gif(self, data):
        if data['error']:
            self.gif_data_frame.show()
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
    mw.show()

    sys.exit(app.exec_())
