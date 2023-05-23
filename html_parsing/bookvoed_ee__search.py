#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


rs = requests.get("https://bookvoed.ee/search?q=white+fang")
root = BeautifulSoup(rs.content, "html.parser")

for row in root.select(".o-row"):
    a = row.select_one("a.title")
    href = urljoin(rs.url, a.get("href"))
    title = a.get_text(strip=True)
    print(title, href)

# White Fang https://bookvoed.ee/goods/4496177
# Белый клык = White Fang https://bookvoed.ee/goods/6807168
# The Call of the Wild and White Fang https://bookvoed.ee/goods/8654867
# White Fang [= Белый Клык] https://bookvoed.ee/goods/451827
# Call of the Wild & White Fang https://bookvoed.ee/goods/4914246
