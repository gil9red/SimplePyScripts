#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт собирает цитаты сайта bash.im"""


import logging
import sys

import requests

from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker


def get_logger(name, file="log.txt", encoding="utf8"):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s"
    )

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)
    return log


logger = get_logger("collector_bash_im")


class Quote:
    def __init__(self, id, date, rating, text) -> None:
        self.id = id
        self.date = date
        self.rating = rating
        self.text = text

    def __repr__(self) -> str:
        return (
            "<Quote(id: {id}. Date: {date}. Rating: '{rating}'. "
            "Text len: {})>".format(len(self.text), **self.__dict__)
        )

    @property
    def url(self):
        return "http://bash.im/quote/" + str(self.id)


def get_session_factory():
    # Создаем базу, включаем логирование и автообновление подключения каждые 2 часа (7200 секунд)
    engine = create_engine(
        # 'sqlite:///:memory:',
        "sqlite:///quotes.db",
        # echo=True,
        pool_recycle=7200,
    )

    metadata = MetaData()

    quotes_table = Table(
        "Quote",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("date", DateTime),
        Column("rating", Integer),
        Column("text", String),
    )

    mapper(Quote, quotes_table)
    metadata.create_all(engine)

    return sessionmaker(bind=engine)


Session = get_session_factory()
session = Session()

query = session.query(Quote)


if __name__ == "__main__":
    rs = requests.get("http://bash.im")
    soup = BeautifulSoup(rs.content, "lxml")
    # print(soup)
    i = 0
    for quote in soup.find_all(attrs={"class": "quote"}):
        text = quote.find(attrs={"class": "text"})
        if not text:
            continue

        i += 1
        # print(quote.find(attrs={"class": "text"}).contents)
        print(i, text)

    sys.exit()

    # xpath = '//*[@class="current"]/*[@class="page"]/@value'
    # current_page = int(g.doc.select(xpath).text())
    # print(current_page)
    #
    # xpath = '//*[@class="quote"]'
    # i = 0
    # for quote in g.doc.select(xpath):
    #     print(quote.text())
    #     nodes = quote.node.find_class('id')
    #     if nodes:
    #         i += 1
    #         quote_id = int(nodes[0].text.replace('#', ''))
    #         date = datetime.strptime(quote.node.find_class('date')[0].text, '%Y-%m-%d %H:%M')
    #         rating = int(quote.node.find_class('rating')[0].text)
    #         text = quote.node.find_class('text')[0]
    #         print(dir(text))
    #         print(text.text_content())
    #         sys.exit()
    #         # print(i, Column(quote_id, date, rating, text))
    #         print(i, quote_id, date, rating, text)
