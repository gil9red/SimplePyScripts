#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Скрипт качает цитаты Конфуция из викицитатника.


from urllib.parse import quote
from grab import Grab


def get_confucius_quotes():
    url = quote("http://ru.wikiquote.org/wiki/Конфуций", safe="/:")

    g = Grab()
    g.go(url)

    quotes = list()
    for el in g.doc.select("//h2/following-sibling::ul/li"):
        quotes.append(el.text())

    return quotes


if __name__ == "__main__":
    for q in get_confucius_quotes():
        print("'{}'".format(q))
