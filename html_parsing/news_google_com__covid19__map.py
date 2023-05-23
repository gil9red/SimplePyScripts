#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from bs4 import BeautifulSoup
import requests


def parse():
    url = "https://news.google.com/covid19/map?hl=ru&gl=RU&ceid=RU:ru"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"
    }

    def _get_num(item) -> str:
        return re.sub(r"\s+", ".", item.get_text(strip=True))

    rs = requests.get(url, headers=headers)
    root = BeautifulSoup(rs.content, "html.parser")

    item = root.select_one("div.tZjT9b")
    confirmed = _get_num(item.select_one("div.fNm5wd.qs41qe > div.UvMayb"))
    deaths = _get_num(item.select_one("div.fNm5wd.ckqIZ > div.UvMayb"))
    recovered = _get_num(item.select_one("div.fNm5wd.gZvxhb > div.UvMayb"))

    print("Заболевших:   ", confirmed)
    print("Выздоровевших:", recovered)
    print("Умерших:      ", deaths)
    # Заболевших:    3.276.373
    # Выздоровевших: 1.024.529
    # Умерших:       233.998


if __name__ == "__main__":
    parse()
