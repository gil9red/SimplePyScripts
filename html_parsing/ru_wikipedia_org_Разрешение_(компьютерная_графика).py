#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


url = "https://ru.wikipedia.org/wiki/Разрешение_(компьютерная_графика)"

rs = requests.get(url)
root = BeautifulSoup(rs.content, "html.parser")

table = root.select(".wikitable")[0]
for tr in table.select("tbody > tr"):
    tds = tr.select("td")
    if not tds:
        continue

    value = tds[1].get_text(strip=True)
    ratio = tds[2].get_text(strip=True)

    if "4:3" in ratio or "16:9" in ratio:
        print(f"{value} ({ratio})")
