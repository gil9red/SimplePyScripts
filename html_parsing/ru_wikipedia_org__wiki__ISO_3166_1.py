#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from bs4 import BeautifulSoup
import requests


rs = requests.get('https://ru.wikipedia.org/wiki/ISO_3166-1')
root = BeautifulSoup(rs.content, 'html.parser')

for tr in root.select_one('.wikitable').select('tr'):
    td_list = tr.select('td')
    if not td_list:
        continue

    td_country, td_alpha2, td_alpha3, td_num_code, _ = td_list
    country = td_country.get_text(strip=True)
    alpha2 = td_alpha2.get_text(strip=True)
    print(country, alpha2)
