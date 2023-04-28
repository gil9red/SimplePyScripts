#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


def get_parsed_two_column_table_stats(url: str) -> list[tuple[str, str]]:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    table = root.select_one("table")

    items = []

    for tr in table.select("tr"):
        tds = tr.select("td")
        if len(tds) != 3:
            continue

        title_node, description_node = tds[1:]

        title = title_node.text.strip()
        description = description_node.text.strip()

        items.append((title, description))

    items.sort(key=lambda x: x[0])

    return items
