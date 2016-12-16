#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: цену сложно найти, как вариант, можно использовать qwebview

text = 'titan quest'
url = 'https://api4.origin.com/xsearch/store/ru_ru/rus/products?searchTerm=' + text
url = 'https://www.origin.com/rus/ru-ru/search?searchString=' + text
url = 'https://www.origin.com/rus/ru-ru/search?searchString=titan'


# from ghost import Ghost
# ghost = Ghost()
#
# with ghost.start() as session:
#     page, extra_resources = session.open(url)
#
#
# quit()

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *


# Чтобы не было проблем запуска компов с прокси:
QNetworkProxyFactory.setUseSystemConfiguration(True)

# print(QWebSettings.globalSettings().getAttribute(QWebSettings.DeveloperExtrasEnabled))

QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
# QWebSettings.globalSettings().setAttribute(QWebSettings.JavascriptEnabled, True)


app = QApplication([])


class UserAgentWebPage(QWebPage):
    def userAgentForUrl(self, url):
        return "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"


view = QWebView()
view.setPage(UserAgentWebPage())
view.show()

# view = QWebView()
# view.show()

view.load(QUrl(url))

view.loadFinished.connect(lambda x=None: print(x))

# loop = QEventLoop()
# view.loadFinished.connect(loop.quit)
# loop.exec_()
#
# doc = view.page().mainFrame().documentElement()

app.exec()


# import requests
# session = requests.session()
# rs = session.get(url)
# print(rs)
#
# data = rs.json()
# print(data)
#
# for game in data['games']['game']:
#     game_info_url = 'https://data3.origin.com/ocd/{}.ru-ru.rus.ocd'.format(game['path'])
#     print(game_info_url)
#
#     rs = session.get(game_info_url)
#     print(rs)
#     print(rs.json())
#
# # https://data2.origin.com/ocd//titanfall/titanfall/addon/the-final-hours-of-titanfall.ru-ru.rus.ocd
#
# # if not data['totalGamesFound']:
# #     print('Not found game')
# #     quit()
# #
# # for game in data['products']:
# #     print(game['title'], game['price']['amount'] + game['price']['symbol'])
