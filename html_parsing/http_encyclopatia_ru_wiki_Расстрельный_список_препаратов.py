#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

import requests
from bs4 import BeautifulSoup


def is_has(letter: str) -> bool:
    letter = letter.strip().lower()

    return bool(re.match("^[а-яё]$", letter))


rs = requests.get("http://encyclopatia.ru/wiki/Расстрельный_список_препаратов")

root = BeautifulSoup(rs.content, "html.parser")
for span in root.select("h2 > .mw-headline"):
    if not is_has(span.text):
        continue

    print(span.text)

    # Нам нужен ul -- в нем описаны препараты, но чтобы его найти,
    # мы сначала найдем элемент с буквой, а после сам элемент
    # <h2><span>А</span></h2>
    # <ul>
    ul = span.parent.find_next_sibling("ul")
    for li in ul.select("li"):
        print(li.text.strip())

    print()
