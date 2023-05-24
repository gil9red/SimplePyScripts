#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from bs4 import BeautifulSoup
import requests

sys.path.append("..")
from ascii_table__simple_pretty__format import print_pretty_table


rs = requests.get("https://www.tabasco.com/hot-sauces/original-red-sauce/")
root = BeautifulSoup(rs.content, "html.parser")

rows = [("", "NAME", "SCOVILLE RATING")]
for i, el in enumerate(root.select(".scoville-chart__product-text"), 1):
    name, scoville = el.get_text(strip=True, separator="\n").splitlines()
    rows.append((i, name, scoville))

print_pretty_table(rows)
#   |                  NAME | SCOVILLE RATING
# --+-----------------------+----------------
# 1 |              Scorpion |          35,000
# 2 |       Habanero Pepper |           >7000
# 3 |          Original Red |     2500 - 5000
# 4 |              Sriracha |     1000 - 3000
# 5 |       Chipotle Pepper |     1500 - 2500
# 6 | Cayenne Garlic Pepper |     1200 - 2400
# 7 |        Green Jalapeño |      600 - 1200
# 8 |     Buffalo Style Hot |       300 - 900
# 9 |         Sweet & Spicy |       100 - 300
