#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: загрузка настоящей страницы скрыта вызовом js кода, нужно использовать qwebview


# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtWebEngineWidgets import *
#
#
# app = QApplication([])
#
# view = QWebEngineView()
# view.show()
#
# view.loadFinished.connect(lambda x: x and view.page().toHtml(print))
#
# url = "http://www.google.ru"
# view.load(QUrl(url))
#
#
# app.exec()
#
# quit()

# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# from PyQt4.QtWebKit import *
# from PyQt4.QtNetwork import *
#
#
# # Чтобы не было проблем запуска компов с прокси:
# QNetworkProxyFactory.setUseSystemConfiguration(True)
#
# QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
#
#
# app = QApplication([])
#
# view = QWebView()
# view.show()
#
# view.load(QUrl("http://www.google.ru"))
#
# app.exec()




text = 'titan'
url = 'http://gama-gama.ru/search/?searchField=' + text
url = 'http://gama-gama.ru'


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
        return "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"

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


# # import robobrowser
# # browser = robobrowser.RoboBrowser()
# # browser.open(url)
# #
# # print(browser.response)
# # print(browser.parsed)
#
# # import requests
# # rs = requests.get(url)
# # print(rs)
# #
# # from bs4 import BeautifulSoup
# # root = BeautifulSoup(rs.content, 'lxml')
# # print(root)
# #
# # for row in root.select('.catalog-row'):
# #     print(row.select_one('.catalog_name').text, )
