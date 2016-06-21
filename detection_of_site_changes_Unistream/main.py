#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


def get_site_text(url='https://test.api.unistream.com/help/index.html'):
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


def get_hash_from_str(text):
    """Функция возвращает хеш от строки в виде HEX чисел, используя алгоритм sha1."""

    import hashlib
    alg = hashlib.sha1()
    alg.update(text.encode())
    return alg.hexdigest().upper()


def get_diff(str_1, str_2, full=True):
    """
    Функция сравнивает переданные строки и возвращает результат сравнения в html.

    """

    import difflib

    diff_html = ""
    theDiffs = difflib.ndiff(str_1.splitlines(), str_2.splitlines())
    for eachDiff in theDiffs:
        if eachDiff[0] == "-":
            diff_html += "<del>%s</del><br>" % eachDiff[1:].strip()
        elif eachDiff[0] == "+":
            diff_html += "<ins>%s</ins><br>" % eachDiff[1:].strip()

    return """<html><head>
            <meta charset="utf-8">
        </head> <body>""" + diff_html + "</body></html>"

    # from lxml.html.diff import htmldiff
    # return """<html><head>
    #     <meta charset="utf-8">
    # </head> <body>""" + htmldiff(str_1, str_2) + "</body></html>"

    # from difflib import HtmlDiff
    # diff = HtmlDiff()
    #
    # str_lines_1 = str_1.split('\n')
    # str_lines_2 = str_2.split('\n')
    #
    # # diff умеет работать с списками, поэтому строку нужно разбить на списки строк,
    # # например, построчно:
    # if full:
    #     return diff.make_file(str_lines_1, str_lines_2)
    # else:
    #     return diff.make_table(str_lines_1, str_lines_2)


from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class TextRevision(Base):
    """
    Класс описывает таблицу ревизий текста.
    Новая запись в таблице появляется только если предыдущая запись имеет отличия от новой.

    """

    __tablename__ = 'TextRevision'

    id = Column(Integer, primary_key=True)

    text = Column(String)

    # Хеш текста
    text_hash = Column(String)

    # Дата проверки
    datetime = Column(DateTime)

    # Поле описывает разницу с предыдущей ревизией.
    # Содержимым является полноценная html страница
    diff_full = Column(String)

    # Поле описывает разницу с предыдущей ревизией.
    # Содержимым является таблица html страницы
    diff = Column(String)

    def __init__(self, text, other_text=''):
        """
        Конструктор принимает контент и сравниваемый контент, запоминает хеш содержимого,
        текущую дату и время и результат сравнения

        """

        from datetime import datetime

        self.text = text
        self.text_hash = get_hash_from_str(text)
        self.datetime = datetime.today()
        self.diff_full = get_diff(text, other_text)
        self.diff = get_diff(text, other_text, full=False)

    def __repr__(self):
        return "<TextRevision(id: {}, datetime: {}, text_hash: {})>".format(self.id, self.datetime, self.text_hash)


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


session = get_session()


def get_last_revision():
    """Функция возвращает последнуюю запись в таблице TextRevision."""

    return session.query(TextRevision).order_by(TextRevision.id.desc()).first()


def add_text_revision(text):
    """Функция добавляет новую ревизию, предварительно сравнив ее с предыдущей."""

    last = get_last_revision()
    logging.debug('Последняя запись: %s.', last)

    text_revision = None

    # Если таблица пуста
    if last is None:
        text_revision = TextRevision(text)
    else:
        # Если хеши текстов отличаются, добавляем новую ревизию
        if last.text_hash != get_hash_from_str(text):
            logging.debug('Обнаружено изменение, создаю ревизию.')
            open('last.text.html', 'w', encoding='utf-8').write(last.text)
            open('text.html', 'w', encoding='utf-8').write(text)
            text_revision = TextRevision(text, last.text)
            open('text_revision.diff_full.html', 'w', encoding='utf-8').write(text_revision.diff_full)
        else:
            return

    if text_revision:
        session.add(text_revision)
        session.commit()

    return text_revision


if __name__ == '__main__':
    # print(session.query(TextRevision).all())
    # quit()

    logging.debug('Запуск.')

    import time

    while True:
        try:
            logging.debug('Проверка сайта.')
            text = get_site_text()
            add_text_revision(text)
            logging.debug('Проверка закончена.')

            break
            # Задержка каждые 7 часов
            time.sleep(60 * 60 * 7)
        except:
            logging.exception('Error:')
    #
    #
    # # print(session.query(TextRevision).all()[1].diff_full)

    last = get_last_revision()
    print(len(last.text))
    if last:
        open('diff.html', 'w', encoding='utf-8').write(last.diff_full)
