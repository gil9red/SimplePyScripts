#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт проверяет дату обновления прайса на сайте http://www.dns-shop.ru/"""


import os
import re

from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage


def _callable(html) -> None:
    if "price-list-downloader" not in html:
        return

    root = BeautifulSoup(html, "lxml")

    for a in root.select("#price-list-downloader a"):
        href = a["href"]

        if href.endswith(".xls"):
            file_url = urljoin(url, href)

            update_date_text = a.next_sibling.strip()

            match = re.search(r"\d{,2}.\d{,2}.\d{4}", update_date_text)
            if match is None:
                return

            date_string = match.group()
            file_name = os.path.basename(href)
            file_name = date_string + "_" + file_name

            print(datetime.today().date(), file_name, file_url)


url = "http://www.dns-shop.ru/"

app = QApplication([])
page = QWebEnginePage()
page.load(QUrl(url))
page.loadFinished.connect(lambda x=None: page.toHtml(_callable))

# Настроим вызов загрузки страницы на каждые 10 часов
timer = QTimer()
timer.setInterval(10 * 60 * 60 * 1000)
timer.timeout.connect(lambda x=None: page.load(QUrl(url)))
timer.start()

app.exec()
