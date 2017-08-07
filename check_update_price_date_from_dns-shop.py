#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт проверяет дату обновления прайса на сайте http://www.dns-shop.ru/"""


# # Основа взята из http://stackoverflow.com/a/37755811/5909792
# def get_html(url, check_content_func=None):
#     # from PyQt5.QtCore import QUrl
#     # from PyQt5.QtWidgets import QApplication
#     # from PyQt5.QtWebEngineWidgets import QWebEnginePage
#
#     from PyQt4.QtCore import QUrl
#     from PyQt4.QtGui import QApplication
#     from PyQt4.QtWebKit import QWebPage as QWebEnginePage
#
#     class ExtractorHtml:
#         def __init__(self, url):
#             self.html = None
#
#             _app = QApplication([])
#             self._page = QWebEnginePage()
#             self._page.mainFrame().load(QUrl(url))
#             # self._page.load(QUrl(url))
#             self._page.loadFinished.connect(self._load_finished_handler)
#
#             # Ожидание загрузки страницы и получения его содержимого
#             # Этот цикл асинхронный код делает синхронным
#             while self.html is None:
#                 _app.processEvents()
#
#             _app.quit()
#
#             self._page = None
#
#         def _callable(self, data):
#             if check_content_func:
#                 if check_content_func(data):
#                     self.html = data
#
#             else:
#                 self.html = data
#
#         def _load_finished_handler(self):
#             # self._page.toHtml(self._callable)
#             self.html = self._page.mainFrame().toHtml()
#
#     return ExtractorHtml(url).html
#
#
# class UpdateDateTextNotFound(Exception):
#     pass
#
#
# import os
#
#
# def download_price():
#     url = 'http://www.dns-shop.ru/'
#
#     html = get_html(url, lambda html: 'price-list-downloader' in html)
#
#     from bs4 import BeautifulSoup
#     root = BeautifulSoup(html, 'lxml')
#
#     for a in root.select('#price-list-downloader a'):
#         href = a['href']
#
#         if href.endswith('.xls'):
#             from urllib.parse import urljoin
#             file_url = urljoin(url, href)
#             # print(file_url)
#
#             update_date_text = a.next_sibling.strip()
#
#             import re
#             match = re.search(r'\d{,2}.\d{,2}.\d{4}', update_date_text)
#             if match is None:
#                 raise UpdateDateTextNotFound()
#
#             date_string = match.group()
#             # print(date_string)
#
#             # from datetime import datetime
#             # print(datetime.strptime(date_string, '%d.%m.%Y'))
#
#             file_name = os.path.basename(href)
#             file_name = date_string + '_' + file_name
#
#             if os.path.exists(file_name):
#                 return file_name
#
#             from urllib.request import urlretrieve
#             urlretrieve(file_url, file_name)
#
#             return file_name
#
#     return
#
#
# while True:
#     file_name = download_price()
#     print(file_name)
#
#     import time
#     # time.sleep(10 * 60 * 60)
#     time.sleep(60)


from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage


def _callable(html):
    if 'price-list-downloader' not in html:
        return

    from bs4 import BeautifulSoup
    root = BeautifulSoup(html, 'lxml')

    for a in root.select('#price-list-downloader a'):
        href = a['href']

        if href.endswith('.xls'):
            from urllib.parse import urljoin
            file_url = urljoin(url, href)

            update_date_text = a.next_sibling.strip()

            import re
            match = re.search(r'\d{,2}.\d{,2}.\d{4}', update_date_text)
            if match is None:
                return

            date_string = match.group()

            import os
            file_name = os.path.basename(href)
            file_name = date_string + '_' + file_name

            from datetime import datetime
            print(datetime.today().date(), file_name, file_url)


url = 'http://www.dns-shop.ru/'

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

