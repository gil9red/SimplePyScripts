#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


rs = requests.get('https://darksouls.fandom.com/ru/wiki/Костер')
root = BeautifulSoup(rs.content, 'html.parser')

for h2 in root.select('h2'):
    headline = h2.select_one('.mw-headline')
    if not headline:
        continue

    if headline.get_text(strip=True) != 'Список костров':
        continue

    for li in h2.find_next_sibling('ol').select('li'):
        print(li.get_text(strip=True, separator=' '))
