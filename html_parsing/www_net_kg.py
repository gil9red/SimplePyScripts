#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


def get_text(tag):
    if not tag:
        return ""

    return tag.get_text(strip=True)


rs = requests.get("https://www.net.kg/")
root = BeautifulSoup(rs.content, "html.parser")

table = root.select_one("#main_block > table:nth-child(27)")

items = []

for tr in table.select("tr"):
    td_list = tr.select("td")
    if not td_list:
        continue

    pos, _, site, kg_hits, hits, visitors, hosts, _ = td_list
    if not site.a.has_attr("title"):
        continue

    items.append((
        get_text(pos),
        site.a["title"],
        get_text(kg_hits),
        get_text(hits),
        get_text(visitors),
        get_text(hosts),
    ))

print(items)
# [('1', 'http://mashina.kg', '425065(+17510)', '487000(+21691)', '38624(+1355)', '12222(+140)'),
#  ('2', 'http://diesel.elcat.kg', '343306(-18716)', '362302(-22870)', '28062(-630)', '14393(-439)'),
#  ...
