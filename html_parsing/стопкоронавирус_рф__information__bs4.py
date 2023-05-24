#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import sys

import requests
from bs4 import BeautifulSoup


rs = requests.get("https://стопкоронавирус.рф/information/")
root = BeautifulSoup(rs.content, "html.parser")

stats = root.select_one("cv-stats-virus")
if not stats:
    print('Not found "cv-stats-virus"!')
    sys.exit()

data = stats[":charts-data"]
data = json.loads(data)
print(data)
# [{'date': '01.05.2020', 'sick': 114431, 'healed': 13220, 'died': 1169}, ...

for x in data:
    print(x["date"], x["sick"], x["healed"], x["died"])
    # 01.05.2020 114431 13220 1169
    # 30.04.2020 106498 11619 1073
    # 29.04.2020 99399 10286 972
    # ...
