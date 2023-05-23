#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get(s: requests.Session, url: str) -> tuple[requests.Response, BeautifulSoup]:
    rs = s.get(url)
    time.sleep(0.3)

    return rs, BeautifulSoup(rs.content, "html.parser")


def get_count_sublist(s: requests.Session, url: str) -> int:
    _, root = get(s, url)
    return sum(int(x.text[1:-1]) for x in root.select(".left-list > li > .c1"))


def url_join(a) -> str:
    return urljoin(URL, a["href"])


URL = "http://lists.memo.ru/index.htm"

s = requests.session()
_, root = get(s, URL)

letter_by_number = dict()

for a in root.select(".alefbet > a"):
    url = url_join(a)
    _, root = get(s, url)

    letter = a.text

    number = 0
    for a in root.select(".doppoisk > a"):
        number += get_count_sublist(s, url_join(a))

    letter_by_number[letter] = number

print("Total:", sum(letter_by_number.values()))
for k, v in letter_by_number.items():
    print(f"{k}: {v}")

# Total: 2734132
# А: 144478
# Б: 229198
# В: 118993
# Г: 186973
# Д: 113005
# Е: 41490
# Ж: 29676
# З: 68842
# И: 63419
# Й: 11
# К: 339774
# Л: 105688
# М: 215806
# Н: 73701
# О: 40130
# П: 157667
# Р: 83422
# С: 212900
# Т: 99711
# У: 30562
# Ф: 58917
# Х: 59343
# Ц: 19324
# Ч: 49970
# Ш: 115709
# Щ: 8615
# Ы: 12
# Э: 21452
# Ю: 15554
# Я: 29790
