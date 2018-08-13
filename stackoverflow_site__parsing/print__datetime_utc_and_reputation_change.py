#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


url = 'https://ru.stackoverflow.com/users/201445/gil9red?tab=reputation'

rs = requests.get(url)
root = BeautifulSoup(rs.content, 'html.parser')

for row in root.select('.rep-table-row'):
    day = row.select_one('.rep-day')['title']
    rep = row.select_one('.rep-cell').text.strip()
    print(day, rep)
