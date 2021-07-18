#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


url = 'https://ru.wiktionary.org/wiki/Приложение:Список_частотных_слов_русского_языка_(2013)'

rs = requests.get(url)
root = BeautifulSoup(rs.content, 'html.parser')

words = [
    x.text
    for x in root.select_one('.wikitable').select('tbody > tr > td:nth-child(2)')
]
print(len(words), words)
