#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


text = 'resident evil 6'

# category1 = 998 (Game)
url = 'http://store.steampowered.com/search/?category1=998&os=win&supportedlang=english&term=' + text

import requests
rs = requests.get(url)
print(rs)

from bs4 import BeautifulSoup
root = BeautifulSoup(rs.content, 'lxml')

for div in root.select('.search_result_row'):
    print(div.select_one('.title').text.strip(), div.select_one('.search_price').text.strip())
