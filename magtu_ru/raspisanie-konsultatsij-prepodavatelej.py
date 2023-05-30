#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


url = "http://www.magtu.ru/student/bakalavriat-spetsialitet-magistratura/raspisanie-konsultatsij-prepodavatelej.html"
rs = requests.get(url)

root = BeautifulSoup(rs.content, "html.parser")
for tag in root.select("[itemprop=articleBody] > *"):
    name = tag.name

    if name == "h3":
        print(tag.text.upper())
        continue

    elif name == "p":
        print(tag.text)
        continue

    elif name == "ul":
        for li in tag.select("li"):
            if li.a:
                print('    "{}": {}'.format(li.a.text, urljoin(rs.url, li.a["href"])))
            else:
                print('    "{}"'.format(li.text))

        print()
        continue
