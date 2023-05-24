#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re

import requests
from bs4 import BeautifulSoup


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"

links_product = ["https://www.wildberries.ru/catalog/10842147/detail.aspx?targetUrl=GP"]
for url in links_product:
    response = session.get(url, timeout=10)
    if response.status_code != 200:
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    js_scripts = soup.find_all("script")
    js_script = str(js_scripts[20])

    m = re.search("ssrModel: (.+),", js_script)
    data = json.loads(m.group(1))
    print(data["suppliersInfo"]["10842147"])
    # {'cod1S': 10842147, 'supplierName': 'ВАЙЛДБЕРРИЗ ООО', 'ogrn': '1067746062449'}
