#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: цену сложно найти, как вариант, можно использовать qwebview


# 1.
url = 'https://api3.origin.com/xsearch/store/ru_ru/rus/products?searchTerm=Kingdoms%20of%20Amalur:%20Reckoning%E2%84%A2%20-%20The'

# 2.
# url = 'https://data1.origin.com/ocd//kingdoms-of-amalur-reckoning/kingdoms-of-amalur-reckoning/addon/kingdoms-of-amalur-reckoning--the-legend-of-dead-kel.ru-ru.rus.ocd'
url = 'https://api3.origin.com/ecommerce2/public/offerId/kingdoms-of-amalur-reckoning/kingdoms-of-amalur-reckoning/addon/kingdoms-of-amalur-reckoning--the-legend-of-dead-kel.RU'

# 3.
url = 'https://api3.origin.com/supercarp/rating/offers/anonymous?country=RU&locale=ru_RU&pid=&currency=RUB&offerIds=OFB-EAST:45293'


import requests
rs = requests.get(url)
# print(rs.text)
print(rs.json())

import pprint
pprint.pprint(rs.json())

# from bs4 import BeautifulSoup
# root = BeautifulSoup(rs.text, 'lxml')
# print(root.prettify())

quit()


url = 'https://www.origin.com/rus/ru-ru/search?searchString=titan'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *


# Чтобы не было проблем запуска компов с прокси:
QNetworkProxyFactory.setUseSystemConfiguration(True)

QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
# QWebSettings.globalSettings().setAttribute(QWebSettings.JavascriptEnabled, True)


app = QApplication([])


class UserAgentWebPage(QWebPage):
    def userAgentForUrl(self, url):
        # return "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
        return 'Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'

    def javaScriptConsoleMessage(self, msg, line, source):
        print('%s line %d: %s' % (source, line, msg))


view = QWebView()
view.setPage(UserAgentWebPage())
view.page().networkAccessManager().setCookieJar(QNetworkCookieJar())

view.show()

# url = 'http://www.whoishostingthis.com/tools/user-agent/'
view.load(QUrl(url))

view.loadFinished.connect(lambda x=None: print(x, view.page().mainFrame().documentElement().toOuterXml().encode()))
view.loadProgress.connect(lambda x=None: print(x))


def sslErrorHandler(qnr, errlist):
    print("--- sslErrorHandler: ")
    for err in errlist:
        print("ssl error:", err)

    qnr.ignoreSslErrors()

view.page().networkAccessManager().sslErrors.connect(sslErrorHandler)


# loop = QEventLoop()
# view.loadFinished.connect(loop.quit)
# loop.exec_()
#
# doc = view.page().mainFrame().documentElement()

app.exec()


# text = 'titan quest'
# url = 'https://api4.origin.com/xsearch/store/ru_ru/rus/products?searchTerm=' + text
# url = 'https://www.origin.com/rus/ru-ru/search?searchString=' + text
# url = 'https://www.origin.com/rus/ru-ru/search?searchString=titan'
#
#
# # from ghost import Ghost
# # ghost = Ghost()
# #
# # with ghost.start() as session:
# #     page, extra_resources = session.open(url)
# #
# #
# # quit()
#
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# from PyQt4.QtWebKit import *
# from PyQt4.QtNetwork import *
#
#
# # Чтобы не было проблем запуска компов с прокси:
# QNetworkProxyFactory.setUseSystemConfiguration(True)
#
# # print(QWebSettings.globalSettings().getAttribute(QWebSettings.DeveloperExtrasEnabled))
#
# QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
# # QWebSettings.globalSettings().setAttribute(QWebSettings.JavascriptEnabled, True)
#
#
# app = QApplication([])
#
#
# class UserAgentWebPage(QWebPage):
#     def userAgentForUrl(self, url):
#         return "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
#
#
# view = QWebView()
# view.setPage(UserAgentWebPage())
# view.show()
#
# # view = QWebView()
# # view.show()
#
# view.load(QUrl(url))
#
# view.loadFinished.connect(lambda x=None: print(x))
#
# # loop = QEventLoop()
# # view.loadFinished.connect(loop.quit)
# # loop.exec_()
# #
# # doc = view.page().mainFrame().documentElement()
#
# app.exec()
#
#
# # import requests
# # session = requests.session()
# # rs = session.get(url)
# # print(rs)
# #
# # data = rs.json()
# # print(data)
# #
# # for game in data['games']['game']:
# #     game_info_url = 'https://data3.origin.com/ocd/{}.ru-ru.rus.ocd'.format(game['path'])
# #     print(game_info_url)
# #
# #     rs = session.get(game_info_url)
# #     print(rs)
# #     print(rs.json())
# #
# # # https://data2.origin.com/ocd//titanfall/titanfall/addon/the-final-hours-of-titanfall.ru-ru.rus.ocd
# #
# # # if not data['totalGamesFound']:
# # #     print('Not found game')
# # #     quit()
# # #
# # # for game in data['products']:
# # #     print(game['title'], game['price']['amount'] + game['price']['symbol'])
