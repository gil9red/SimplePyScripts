#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


rs = requests.get("https://mikafood.ru/")
root = BeautifulSoup(rs.content, "html.parser")

items = [
    (x.text.strip(), x["href"])
    for x in root.select(".box-menu-content .name > a")
]

# Находим максимальную ширину первого столбца
print_format = "{:%s} {}" % (max(len(x[0]) for x in items),)

for title, url in items:
    print(print_format.format(title, url))
