#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


url = "https://www.banki.ru/products/currency/cb/"

rs = requests.get(url)
root = BeautifulSoup(rs.content, "html.parser")

for tr in root.select("tbody > tr[data-currency-code]"):
    td_items = tr.select("td")
    code, num, name, value, change = map(lambda x: x.get_text(strip=True), td_items)
    print(code, num, name, value, change)

# USD 1 Доллар США 73.4261 +0,0628
# EUR 1 Евро 87.2889 +1,0357
# AUD 1 Австралийский доллар 52.8154 +0,4633
# ...
# ZAR 10 Южноафриканский рэнд 43.4922 -0,2144
# JPY 100 Японская иена 70.1870 +0,3803
