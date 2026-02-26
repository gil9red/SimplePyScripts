#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup

from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage


# Основа взята из http://stackoverflow.com/a/37755811/5909792
def get_html(url):
    class ExtractorHtml:
        def __init__(self, url) -> None:
            _app = QApplication([])
            self._page = QWebEnginePage()

            self.html = None

            # Небольшой костыль для получения содержимого страницы сайта
            # https://www.origin.com/rus/ru-ru/search?searchString=
            # Загрузка страницы проходит постепенно -- данные не сразу появляются, поэтому нужно
            # подождать пока они закончатся загружаться. Для этого заводится таймер, который дает по 5 секунд
            # после каждой закончившееся загрузки чтобы после вытащить данные из страницы
            timer = QTimer()
            timer.setSingleShot(True)
            timer.setInterval(5000)
            timer.timeout.connect(self._load_finished_handler)

            self._page.loadProgress.connect(lambda x: x == 100 and timer.start())

            self._page.load(QUrl(url))

            # Ожидание загрузки страницы и получения его содержимого
            # Этот цикл асинхронный код делает синхронным
            while self.html is None:
                _app.processEvents()

            _app.quit()

            self._page = None

        def _callable(self, data) -> None:
            self.html = data

        def _load_finished_handler(self) -> None:
            self._page.toHtml(self._callable)

    return ExtractorHtml(url).html


text = "titan"
url = f"https://www.origin.com/rus/ru-ru/search?searchString={text}"

html = get_html(url)
root = BeautifulSoup(html, "lxml")

for game in root.select(".origin-search-section .origin-storegametile-details"):
    name = game.select_one(".origin-storegametile-title").text.strip()
    price = None

    storeprice = game.select_one(".origin-storeprice")

    otkprice = storeprice.select_one(".otkprice")
    if otkprice:
        price = otkprice.text.strip()
    else:
        free = storeprice.select_one(".otkprice-free")
        if free:
            price = 0

    print(name, price)
