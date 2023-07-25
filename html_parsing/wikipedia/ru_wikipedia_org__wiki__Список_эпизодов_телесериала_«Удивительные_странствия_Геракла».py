#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


url = "https://ru.wikipedia.org/wiki/Список_эпизодов_телесериала_«Удивительные_странствия_Геракла»"

rs = requests.get(url)
root = BeautifulSoup(rs.content, "html.parser")

seasons_by_number = dict()

for span in root.select("span.mw-headline"):
    if "Сезон" not in span.text:
        continue

    tr_items = span.parent.find_next_sibling("table").find_all("tr")
    seasons_by_number[span.text] = len(tr_items) - 1

print(f"Seasons: {len(seasons_by_number)}")
print(f"Series: {sum(seasons_by_number.values())}\n")
for k, v in seasons_by_number.items():
    print(f"{k}: {v}")

# Seasons: 6
# Series: 111
#
# Сезон 1 (1995): 13
# Сезон 2 (1995—1996): 24
# Сезон 3 (1996—1997): 22
# Сезон 4 (1997—1998): 22
# Сезон 5 (1998—1999): 22
# Сезон 6 (1999): 8
