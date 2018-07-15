#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


url = 'https://ru.wikipedia.org/wiki/Список_серий_«Наруто»_(сезоны_1—3)'

import requests
rs = requests.get(url)

from bs4 import BeautifulSoup
root = BeautifulSoup(rs.content, 'html.parser')

td_list = []

for td in root.select('td'):
    if td.has_attr('id') and td['id'].startswith('ep'):
        td_list.append(td)
        print(td)
