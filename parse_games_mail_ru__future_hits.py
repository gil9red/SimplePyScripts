#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
rs = requests.get('https://games.mail.ru/pc/games/future_hits/')

from bs4 import BeautifulSoup
root = BeautifulSoup(rs.content, 'lxml')

# Перебор табличек с играми
for i, item in enumerate(root.select('.b-pc__entities-item'), 1):
    a = item.select_one('.b-pc__entities-title > a')
    title = a.text.strip()

    from urllib.parse import urljoin
    url = urljoin(rs.url, a['href'])

    description = item.select_one('.b-pc__entities-descr').text.strip()
    img_url = item.select_one('.b-pc__entities-img')['src']
    release_date = item.select_one('.b-pc__entities-author').text.strip()

    print('{:2}. "{}" ({}): {} {}\n{}\n'.format(i, title, release_date, url, img_url, description))
