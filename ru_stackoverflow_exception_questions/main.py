#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт добавляет метку 'исключения' для указанных вопросов."""


def get_logger(name, file='log.txt', encoding='utf8'):
    import logging
    import sys

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)
    return log


logger = get_logger('so_questions')


import json
config = json.load(open('config', encoding='utf8'))
LOGIN = config['login']
PASSWORD = config['password']

#
# import time
# import traceback


from gatherer import query


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36 Gt/{32}'


if __name__ == '__main__':


# from PySide.QtCore import *
# from PySide.QtGui import *
# from PySide.QtWebKit import *
# from PySide.QtNetwork import *
#
# # Чтобы не было проблем запуска компов с прокси:
# QNetworkProxyFactory.setUseSystemConfiguration(True)
#
# QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
#
# self.view = QWebView()
# self.setCentralWidget(self.view)
#
# self.view.show()
#
# self.view.load('https://ru.stackoverflow.com/users/login')
#
# # Ждем пока прогрузится страница
# loop = QEventLoop()
# self.view.loadFinished.connect(loop.quit)
# loop.exec_()
#
# self.doc = self.view.page().mainFrame().documentElement()
# self.doc.findFirst('#email').setAttribute("value", "ilya.petrash@inbox.ru")
# self.doc.findFirst('#password').setAttribute("value", "FastFood!921874")
# self.doc.findFirst('#submit-button').evaluateJavaScript('this.click()');
#
#
# self.view.load('http://ru.stackoverflow.com/questions/137')
#
# # Ждем пока прогрузится страница
# loop = QEventLoop()
# self.view.loadFinished.connect(loop.quit)
# loop.exec_()
#
# self.doc = self.view.page().mainFrame().documentElement()
#
# # Кликаем на "править"
# href = self.doc.findFirst('.question .suggest-edit-post').attribute('href')
# js = 'window.location.href = "{}";'.format(href)
# print(href, js)
# self.doc.evaluateJavaScript(js);
#
# # Ждем пока прогрузится страница
# loop = QEventLoop()
# self.view.loadFinished.connect(loop.quit)
# loop.exec_()
#
# self.doc = self.view.page().mainFrame().documentElement()
# js = '$(".tag-editor input")[0].value = "{}";'.format("исключения")
# self.doc.evaluateJavaScript(js);
#
# # TODO: надо как то сэмулировать создание метки
# #js = '$(".wmd-input.processed")[0].focus();'
# #self.doc.evaluateJavaScript(js);
#
# # TODO: или вручную создать dom элементы, для описания метки
# #print(self.doc.findFirst(".tag-editor span").isNull())
#
# # Добавление описания метки
# js = '$("#edit-comment")[0].value = "{}";'.format('Добавлена метка: исключения')
# self.doc.evaluateJavaScript(js);
#

    print(query.all()[0].url)
    print(query.count())
    # print(query.all())
    quit()

    import sys

    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtNetwork import *
    from PySide.QtWebKit import *

    app = QApplication(sys.argv)

    url = ''

    request = QNetworkRequest()
    request.setUrl(QUrl(url))
    request.setRawHeader("User-Agent", USER_AGENT)

    webkit = QWebView()
    webkit.load(request)

    sys.exit(app.exec_())
