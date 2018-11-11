#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


rs = requests.get('https://en.wikipedia.org/wiki/Darksiders_(series)')
root = BeautifulSoup(rs.content, 'html.parser')

table = root.select_one('.wikitable')

# Timeline of release years
for tr in table.select('tr'):
    td_items = tr.select('td')
    if len(td_items) != 2:
        continue

    year = td_items[0].text.strip()
    name = td_items[1].i.text.strip()
    print(year, name)
