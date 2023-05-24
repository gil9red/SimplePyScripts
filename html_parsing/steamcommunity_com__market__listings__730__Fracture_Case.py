#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re

import requests


rs = requests.get("https://steamcommunity.com/market/listings/730/Fracture Case")

m = re.search(r"var line1=(.+);", rs.text)
data_str = m.group(1)

data = json.loads(data_str)
print(data)
# [['Aug 07 2020 01: +0', 10.698, '57688'], ['Aug 08 2020 01: +0', 6.926, '48599'], ...

print(data[0])
# ['Aug 07 2020 01: +0', 10.698, '57688']

print(data[-1])
# ['Sep 10 2020 10: +0', 1.39, '1451']
