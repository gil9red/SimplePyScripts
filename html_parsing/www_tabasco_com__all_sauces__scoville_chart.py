#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup

# pip install tabulate
from tabulate import tabulate


rs = requests.get("https://www.tabasco.com/hot-sauces/original-red-sauce/")
root = BeautifulSoup(rs.content, "html.parser")

rows = []
for i, el in enumerate(root.select(".scoville-chart__product-text"), 1):
    name, scoville = el.get_text(strip=True, separator="\n").splitlines()
    rows.append((i, name, scoville))

print(tabulate(rows, headers=("", "NAME", "SCOVILLE RATING"), tablefmt="grid"))
"""
+----+-------------------+-------------------+
|    | NAME              | SCOVILLE RATING   |
+====+===================+===================+
|  1 | Scorpion          | 23,000-33,000     |
+----+-------------------+-------------------+
|  2 | Habanero Pepper   | >7000             |
+----+-------------------+-------------------+
|  3 | Original Red      | 2500 - 5000       |
+----+-------------------+-------------------+
|  4 | Sriracha          | 1000 - 3000       |
+----+-------------------+-------------------+
|  5 | Chipotle Pepper   | 1500 - 2500       |
+----+-------------------+-------------------+
|  6 | Cayenne Garlic    | 1200 - 2400       |
+----+-------------------+-------------------+
|  7 | Green Jalapeño    | 600 - 1200        |
+----+-------------------+-------------------+
|  8 | Buffalo Style Hot | 300 - 900         |
+----+-------------------+-------------------+
|  9 | Sweet & Spicy     | 100 - 600         |
+----+-------------------+-------------------+
"""
