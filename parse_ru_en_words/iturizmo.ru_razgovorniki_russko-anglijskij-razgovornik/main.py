#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
rs = requests.get('http://iturizmo.ru/razgovorniki/russko-anglijskij-razgovornik.html')

from bs4 import BeautifulSoup
root = BeautifulSoup(rs.content, 'html.parser')

ru_en_items = []

for tr in root.select(".entry-content tr"):
    td_list = [td.text for td in tr.select('td')]
    if not td_list:
        continue

    ru, en = td_list[:2]
    ru_en_items.append((ru, en))

print(len(ru_en_items), ru_en_items)

import json
json.dump(ru_en_items, open('en_ru.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
