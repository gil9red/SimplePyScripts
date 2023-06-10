#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage


# Основа взята из http://stackoverflow.com/a/37755811/5909792
def get_html(url, check_content_func=None):
    class ExtractorHtml:
        def __init__(self, url):
            self.html = None

            _app = QApplication([])
            self._page = QWebEnginePage()
            self._page.load(QUrl(url))
            self._page.loadFinished.connect(self._load_finished_handler)

            # Ожидание загрузки страницы и получения его содержимого
            # Этот цикл асинхронный код делает синхронным
            while self.html is None:
                _app.processEvents()

            _app.quit()

            self._page = None

        def _callable(self, data):
            if check_content_func:
                if check_content_func(data):
                    self.html = data

            else:
                self.html = data

        def _load_finished_handler(self):
            self._page.toHtml(self._callable)

    return ExtractorHtml(url).html


url = "http://www.dns-shop.ru/"
html = get_html(url, lambda html: "price-list-downloader" in html)
print(html)
