#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models.expressions import Date

__author__ = 'ipetrash'


import sys

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s',
    handlers=[
        logging.FileHandler('log', encoding='utf8'),
        logging.StreamHandler(stream=sys.stdout),
    ],
)


def get_site_content(url='https://test.api.unistream.com/help/index.html'):
    """Функция возвращает содержимое по указанному url."""

    import sys

    from PySide.QtGui import QApplication
    from PySide.QtCore import QEventLoop
    from PySide.QtWebKit import QWebSettings, QWebPage, QWebView
    from PySide.QtNetwork import QNetworkProxyFactory

    # Чтобы не было проблем запуска компов с прокси:
    QNetworkProxyFactory.setUseSystemConfiguration(True)

    QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

    class WebPage(QWebPage):
        def userAgentForUrl(self, url):
            return 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'

    QApplication(sys.argv)

    view = QWebView()
    view.setPage(WebPage())
    view.load(url)

    # Ждем пока прогрузится страница
    loop = QEventLoop()
    view.loadFinished.connect(loop.quit)
    loop.exec_()

    doc = view.page().mainFrame().documentElement()
    return doc.toOuterXml()


def hash_from_str(text):
    """Функция возвращает хэш от строки в виде HEX чисел, используя алгоритм sha1."""

    import hashlib
    alg = hashlib.sha1()
    alg.update(text.encode())
    return alg.hexdigest().upper()


def get_diff(str_1, str_2):
    """
    Функция сравнивает переданные строки и возвращает результат сравнения в html.

    """

    from difflib import HtmlDiff
    diff = HtmlDiff()

    # diff умеет работать с списками, поэтому строку нужно разбить на списки строк,
    # например, построчно:
    return diff.make_file(str_1.split('\n'), str_2.split('\n'))


from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class ContentRevision(Base):
    """
    Класс описывает таблицу ревизий содержимого.
    Новая запись в таблице появляется только если предыдущая запись имеет отличия от новой.

    """

    __tablename__ = 'ContentRevision'

    id = Column(Integer, primary_key=True)

    # Содержимое
    content = Column(String)

    # Хэш содержимого
    content_hash = Column(String)

    # Дата проверки содержимого
    date = Column(Date)

    # Поле описывает разницу с предыдущей ревизией.
    # Содержимым является полноценная html страница
    diff = Column(String)
    
    def __init__(self, content, content_hash, date, diff):
        self.content = content
        self.content_hash = content_hash
        self.date = date
        self.diff = diff

    def __repr__(self):
        return "<ContentRevision(id: {}, date: %s, hash: %s)>".format(self.id, self.date, self.hash)


def get_session():
    import os
    DIR = os.path.dirname(__file__)
    DB_FILE_NAME = 'sqlite:///' + os.path.join(DIR, 'database')
    # DB_FILE_NAME = 'sqlite:///:memory:'

    # Создаем базу, включаем логирование и автообновление подключения каждые 2 часа (7200 секунд)
    from sqlalchemy import create_engine
    engine = create_engine(
        DB_FILE_NAME,
        # echo=True,
        pool_recycle=7200
    )

    Base.metadata.create_all(engine)

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == '__main__':
    print(get_site_content())

    # import time
    #
    # while True:
    #     # Задержка каждые 7 часов
    #     time.sleep(60 * 60 * 7)
    #
    # # session = get_session()
    # #
    # # # session.add(User("dfdf", 'dfdf', '223'))
    # # # session.commit()
    # #
    # # print(session.query(ContentRevision).all())

