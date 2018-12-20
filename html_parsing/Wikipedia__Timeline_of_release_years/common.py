#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Callable, Any

import requests
from bs4 import BeautifulSoup


def get_parsed_two_column_wikitable(url: str, is_match_func: Callable[[Any], bool]=lambda table: True) -> [(str, str)]:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    table = None
    for t in root.select('.wikitable'):
        if not t.caption:
            continue

        if is_match_func(t):
            table = t
            break

    if not table:
        raise Exception('Not found table "Timeline of releases"')

    items = []

    # Timeline of release years
    for tr in table.select('tr'):
        td_items = tr.select('td')
        if len(td_items) != 2:
            continue

        year = td_items[0].text.strip()
        name = td_items[1].i.text.strip()
        items.append((year, name))

    return items
