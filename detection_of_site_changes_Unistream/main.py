#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import difflib
import hashlib
import logging
import os
import sys

from PySide.QtGui import QApplication
from PySide.QtCore import QEventLoop
from PySide.QtWebKit import QWebSettings, QWebPage, QWebView
from PySide.QtNetwork import QNetworkProxyFactory

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# NOTE: костыль для винды, для исправления проблем с исключениями
# при выводе юникодных символов в консоль винды
if sys.platform == "win32":
    import codecs

    # Для винды кодировкой консоли будет cp866
    sys.stdout = codecs.getwriter(sys.stdout.encoding)(
        sys.stdout.detach(), "backslashreplace"
    )
    sys.stderr = codecs.getwriter(sys.stderr.encoding)(
        sys.stderr.detach(), "backslashreplace"
    )


DIR = os.path.dirname(__file__)


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(DIR, "log"), encoding="utf8"),
        logging.StreamHandler(stream=sys.stdout),
    ],
)


def get_site_text(url="https://test.api.unistream.com/help/index.html"):
    """Функция возвращает содержимое по указанному url."""

    # Чтобы не было проблем запуска компов с прокси:
    QNetworkProxyFactory.setUseSystemConfiguration(True)

    QWebSettings.globalSettings().setAttribute(
        QWebSettings.DeveloperExtrasEnabled, True
    )

    class WebPage(QWebPage):
        def userAgentForUrl(self, url):
            return "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"

    if QApplication.instance() is None:
        QApplication(sys.argv)

    view = QWebView()
    view.setPage(WebPage())
    view.load(url)

    # Ждем пока прогрузится страница
    loop = QEventLoop()
    view.loadFinished.connect(loop.quit)
    loop.exec_()

    doc = view.page().mainFrame().documentElement()
    print(len(doc.toOuterXml()), len(doc.toPlainText()))
    return doc.toPlainText()


def get_hash_from_str(text):
    """Функция возвращает хеш от строки в виде HEX чисел, используя алгоритм sha1."""

    alg = hashlib.sha1()
    alg.update(text.encode())
    return alg.hexdigest().upper()


def get_diff(str_1, str_2, full=True):
    """
    Функция сравнивает переданные строки и возвращает результат сравнения в html.

    """

    logging.debug("x1")
    logging.debug("x2")
    diff_html = ""
    logging.debug("x3")
    theDiffs = difflib.ndiff(str_1.splitlines(), str_2.splitlines())

    logging.debug("x4")
    theDiffs = list(theDiffs)
    print(theDiffs)
    for eachDiff in theDiffs:
        if eachDiff[0] == "-":
            diff_html += "<del>%s</del><br>" % eachDiff[1:].strip()
        elif eachDiff[0] == "+":
            diff_html += "<ins>%s</ins><br>" % eachDiff[1:].strip()
    logging.debug("x5")

    print(112121, diff_html)

    if full:
        return (
            """<html><head><meta charset="utf-8"></head> <body>"""
            + diff_html
            + "</body></html>"
        )
    else:
        return diff_html


Base = declarative_base()


class TextRevision(Base):
    """
    Класс описывает таблицу ревизий текста.
    Новая запись в таблице появляется только если предыдущая запись имеет отличия от новой.

    """

    __tablename__ = "TextRevision"

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
    # Содержимым является только разница
    diff = Column(String)

    def __init__(self, new_text, old_text=""):
        """
        Конструктор принимает контент и сравниваемый контент, запоминает хеш содержимого,
        текущую дату и время и результат сравнения

        """

        from datetime import datetime

        self.text = new_text
        self.text_hash = get_hash_from_str(new_text)
        self.datetime = datetime.today()

        # TODO: удалить diff_full и diff -- не используются, к тому что, имея text можно самому сделать сравнение
        self.diff_full = get_diff(old_text, new_text)
        self.diff = get_diff(old_text, new_text, full=False)

    def __repr__(self):
        return f"<TextRevision(id: {self.id}, datetime: {self.datetime}, text_hash: {self.text_hash})>"


def get_session():
    DB_FILE_NAME = "sqlite:///" + os.path.join(DIR, "database")
    # DB_FILE_NAME = 'sqlite:///:memory:'

    # Создаем базу, включаем логирование и автообновление подключения каждые 2 часа (7200 секунд)
    engine = create_engine(
        DB_FILE_NAME,
        # echo=True,
        pool_recycle=7200,
    )

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    return Session()


session = get_session()


def get_last_revision():
    """Функция возвращает последнуюю запись в таблице TextRevision."""

    return session.query(TextRevision).order_by(TextRevision.id.desc()).first()


def add_text_revision(text):
    """Функция добавляет новую ревизию, предварительно сравнив ее с предыдущей."""

    last = get_last_revision()
    logging.debug("Последняя запись: %s.", last)

    # Если таблица пуста
    if last is None:
        text_revision = TextRevision(text)
    else:
        # Если хеши текстов отличаются, добавляем новую ревизию
        if last.text_hash != get_hash_from_str(text):
            logging.debug("Обнаружено изменение, создаю ревизию.")
            text_revision = TextRevision(text, last.text)
            logging.debug("-")
        else:
            logging.debug("Одинаковые значения, пропускаю добавление.")
            return

    logging.debug("@")
    if text_revision:
        logging.debug("add")
        session.add(text_revision)
        logging.debug("commit")
        session.commit()

    logging.debug("return")
    return text_revision


if __name__ == "__main__":
    logging.debug("Запуск.")

    import time

    while True:
        try:
            logging.debug("Проверка сайта.")

            # text = "dfsdfsdfsdfsdf"
            # text += get_site_text()
            # text += "dfsdfsdfsdfsdf"

            text = get_site_text()

            # У сайта есть особенность -- некоторые данные в примерах с каждой загрузки
            # новые, и они портят работу скрипта, но не несут никакой пользы
            # Нужно их удалить.
            # Данные:
            # "OperationId": "ab0ddd72-767d-400c-b17c-811c88c2cdc1",
            # "CommandId": "c4a52a43-8caf-4f51-bcd3-8090fb91b597",
            # "cashierUniqueId": "cc3b8fe2-8ecc-4af4-9076-d5315aa74896",
            # "id": "31f7e9e2-ea4f-469a-a498-379cfcc3fa12",
            # "createTime": "2016-06-22T10:13:42.0888396+03:00",
            # "templateId": "e6635cf6-47c3-4164-8173-cb8fd249604a"
            import re

            text = re.sub(r'"((?i)OperationId)": ".+?"', r'"\1": "<removed>"', text)
            text = re.sub(r'"((?i)CommandId)": ".+?"', r'"\1": "<removed>"', text)
            text = re.sub(r'"((?i)cashierUniqueId)": ".+?"', r'"\1": "<removed>"', text)
            text = re.sub(r'"((?i)id)": ".+?"', r'""\1"": "<removed>"', text)
            text = re.sub(r'"((?i)createTime)": ".+?"', r'"\1": "<removed>"', text)
            text = re.sub(r'"((?i)templateId)": ".+?"', r'"\1": "<removed>"', text)
            if not text:
                continue

            add_text_revision(text)
            logging.debug("Проверка закончена.")

            # last = get_last_revision()
            # print(len(last.text))
            # if last:
            #     open('diff.html', 'w', encoding='utf-8').write(last.diff_full)
            # quit()

            # Задержка каждые 7 часов
            time.sleep(60 * 60 * 7)
        except Exception:
            logging.exception("Error:")

    # last = get_last_revision()
    # print(len(last.text))
    # if last:
    #     open('diff.html', 'w', encoding='utf-8').write(last.diff_full)
