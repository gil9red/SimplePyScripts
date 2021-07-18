#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

import requests
from bs4 import BeautifulSoup


def get_words() -> List[str]:
    url = 'https://ru.wiktionary.org/wiki/Приложение:Список_частотных_слов_русского_языка_(2013)'

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    return [
        x.text
        for x in root.select_one('.wikitable').select('tbody > tr > td:nth-child(2)')
    ]


if __name__ == '__main__':
    words = get_words()
    print(len(words), words)
