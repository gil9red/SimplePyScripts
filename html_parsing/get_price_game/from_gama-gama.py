#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from bs4 import BeautifulSoup

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage


# Основа взята из http://stackoverflow.com/a/37755811/5909792
def get_html(url):
    class ExtractorHtml:
        def __init__(self, url) -> None:
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

        def _callable(self, data) -> None:
            self.html = data

        def _load_finished_handler(self, _) -> None:
            self._counter_finished += 1

            if self._counter_finished == 2:
                self._page.toHtml(self._callable)

    return ExtractorHtml(url).html


text = "mad"
url = f"http://gama-gama.ru/search/?searchField={text}"

html = get_html(url)


root = BeautifulSoup(html, "lxml")

for game in root.select(".catalog-content > a"):
    name = game["title"].strip()
    name = name.replace("Купить ", "")

    price = None
    price_holder = game.select_one(".catalog_price_holder")

    price_1 = price_holder.select_one(".price_1")
    if price_1:
        price = price_1.text.strip()
    else:
        # Содержит описание цены со скидкой. Вытаскиваем цену со скидкой
        price_2 = price_holder.select_one(".price_2")
        if price_2:
            price = price_2.select_one(".price_group > .promo_price").text

            # Удаление пустых символов пробелом
            price = re.sub(r"\s+", " ", price).strip()

    print(name, price)
