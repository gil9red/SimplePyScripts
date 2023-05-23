#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


url = "http://www.radgametools.com/binkgames.htm"
rs = requests.get(url)
root = BeautifulSoup(rs.content, "html.parser")

items = [x.get_text(strip=True) for x in root.select(".gameslist > dl > dt")]
print(f"Items ({len(items)}): {items}")
# Items (403): ['1C', '2015 Inc', '2XL Games', ..., 'Zombie', 'Zoë Mode', 'Zoo Digital Publishing']
