#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage


# Основа взята из http://stackoverflow.com/a/37755811/5909792
def get_html(url):
    class ExtractorHtml:
        def __init__(self, url):
            _app = QApplication([])
            self._page = QWebEnginePage()
            self._page.loadFinished.connect(self._load_finished_handler)

            self.html = None

            # Небольшой костыль для получения содержимого страницы сайта http://gama-gama.ru
            # Загрузка страницы проходит 2 раза: сначада кусок хитрого javascript кода, потом страница
            # сайта с содержимым
            self._counter_finished = 0

            self._page.load(QUrl(url))

            # Ожидание загрузки страницы и получения его содержимого
            # Этот цикл асинхронный код делает синхронным
            while self.html is None:
                _app.processEvents()

            _app.quit()

            # Чтобы избежать падений скрипта
            self._page = None

        def _callable(self, data):
            self.html = data

        def _load_finished_handler(self, _):
            self._counter_finished += 1

            if self._counter_finished == 2:
                self._page.toHtml(self._callable)

    return ExtractorHtml(url).html


if __name__ == "__main__":
    url = "http://gama-gama.ru/search/?searchField=titan"
    print(get_html(url))
