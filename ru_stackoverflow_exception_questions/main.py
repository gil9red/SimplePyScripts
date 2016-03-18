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
