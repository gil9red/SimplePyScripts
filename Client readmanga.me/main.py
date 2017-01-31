#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtWebEngineWidgets import *


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()

import sys
sys.excepthook = log_uncaught_exceptions


def search_manga_on_readmanga(query_text, sort=True):
    import requests
    rs = requests.get('http://readmanga.me/search/suggestion?query=' + query_text)

    search_result_list = rs.json()['suggestions']

    # Фильтрация ссылок: удаление тех, что ведут на авторов
    manga_list = list(filter(lambda item: '/list/person/' not in item['data']['link'], search_result_list))

    # Относительные ссылки на главы делаем абсолютными
    for manga_obj in manga_list:
        rel_url = manga_obj['data']['link']

        from urllib.parse import urljoin
        url = urljoin(rs.url, rel_url)

        manga_obj['data']['link'] = url

    if sort:
        manga_list.sort(key=lambda item: item['value'])

    return manga_list


class MainWindow(QMainWindow):
    ROLE_MANGA_OBJ = Qt.UserRole
    ROLE_MANGA_URL = Qt.UserRole + 1

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Client http://readmanga.me')

        self.line_edit_search = QLineEdit()
        self.line_edit_search.setPlaceholderText('Введите название манги...')
        self.line_edit_search.setClearButtonEnabled(True)
        self.line_edit_search.textEdited.connect(self.on_manga_search)

        self.list_widget_search_result = QListWidget()
        self.list_widget_search_result.itemDoubleClicked.connect(self.on_search_item_double_clicked)

        left_side_layout = QVBoxLayout()
        left_side_layout.addWidget(self.line_edit_search)
        left_side_layout.addWidget(self.list_widget_search_result)

        left_side_widget = QWidget()
        left_side_widget.setLayout(left_side_layout)

        self.web_view = QWebEngineView()

        central_widget = QSplitter(Qt.Horizontal)
        central_widget.addWidget(left_side_widget)
        central_widget.addWidget(self.web_view)

        self.setCentralWidget(central_widget)

    def on_manga_search(self, query_text):
        self.list_widget_search_result.clear()

        manga_list = search_manga_on_readmanga(query_text)

        for manga_obj in manga_list:
            text = manga_obj['value']

            another_names = manga_obj['data']['names']
            if another_names:
                text += " | " + ', '.join(another_names)

            authors = manga_obj['data']['authors']
            if authors:
                text += " (" + authors + ")"

            url = manga_obj['data']['link']

            item = QListWidgetItem(text)
            item.setData(self.ROLE_MANGA_OBJ, manga_obj)
            item.setData(self.ROLE_MANGA_URL, url)

            self.list_widget_search_result.addItem(item)

    def on_search_item_double_clicked(self, item):
        url = item.data(self.ROLE_MANGA_URL)

        self.web_view.load(QUrl(url))


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
