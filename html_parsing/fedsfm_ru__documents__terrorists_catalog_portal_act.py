#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


rs = requests.get("http://www.fedsfm.ru/documents/terrorists-catalog-portal-act")
root = BeautifulSoup(rs.content, "html.parser")

items = [li.text for li in root.select("#russianFL li")]
print(f"Всего: {len(items)}")
# Всего: 12675

print(*items[:3], sep="\n")
print("...")
print(*items[-3:], sep="\n")
