#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Чтобы не было проблем запуска компов с прокси:
    QNetworkProxyFactory.setUseSystemConfiguration(True)

    QWebSettings.globalSettings().setAttribute(
        QWebSettings.DeveloperExtrasEnabled, True
    )

    view = QWebView()
    # view.show()
    view.load("http://www.myscore.ru/match/nqD8D0j4/#match-statistics;0")

    # Ждем пока прогрузится страница
    loop = QEventLoop()
    view.loadFinished.connect(loop.quit)
    loop.exec_()

    doc = view.page().mainFrame().documentElement()
    print(doc.findFirst("#statistics-0-statistic a").toPlainText())
    print(doc.findFirst("#statistics-1-statistic a").toPlainText())
    print(doc.findFirst("#statistics-2-statistic a").toPlainText())

    table = doc.findFirst("#tab-statistics-0-statistic .parts")
    for tr in table.findAll("tr"):
        l, text, r = tr.toPlainText().split("\t")
        print(l, text, r)

    # sys.exit(app.exec_())
