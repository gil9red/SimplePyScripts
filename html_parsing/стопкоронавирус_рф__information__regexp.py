#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re
import sys

import requests


rs = requests.get("https://стопкоронавирус.рф/information/")
m = re.search(":charts-data='(.+?)'", rs.text)
if not m:
    print('Not found "charts-data"!')
    sys.exit()

data = json.loads(m.group(1))
print(data)
# [{'date': '01.05.2020', 'sick': 114431, 'healed': 13220, 'died': 1169}, ...

for x in data:
    print(x["date"], x["sick"], x["healed"], x["died"])
    # 01.05.2020 114431 13220 1169
    # 30.04.2020 106498 11619 1073
    # 29.04.2020 99399 10286 972
    # ...
