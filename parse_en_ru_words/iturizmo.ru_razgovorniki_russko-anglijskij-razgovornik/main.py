#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
rs = requests.get('http://iturizmo.ru/razgovorniki/russko-anglijskij-razgovornik.html')

from bs4 import BeautifulSoup
root = BeautifulSoup(rs.content, 'html.parser')

en_ru_items = []

for tr in root.select(".entry-content tr"):
    td_list = [td.text.strip() for td in tr.select('td')]
    if not td_list:
        continue

    ru, en = td_list[:2]
    en_ru_items.append((en, ru))

print(len(en_ru_items), en_ru_items)

import json
json.dump(en_ru_items, open('en_ru.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
