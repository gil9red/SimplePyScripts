#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import Callable, Any

import requests
from bs4 import BeautifulSoup, Tag


MatchFunc = Callable[[Any], bool]


def find_table(
    url: str,
    is_match_table_func: MatchFunc = lambda table: True,
) -> Tag | None:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    for t in root.select(".wikitable"):
        if not t.caption:
            continue

        if is_match_table_func(t):
            return t

    return


def get_parsed_two_column_wikitable(
    url: str,
    is_match_table_func: MatchFunc = lambda table: True,
    is_match_row_func: MatchFunc = lambda tr: True,
) -> list[tuple[str, str]]:
    table = find_table(url, is_match_table_func)
    if not table:
        raise Exception('Not found table "Timeline of releases"')

    items = []

    year = None

    # Timeline of release years
    for tr in table.select("tr"):
        td_items = tr.select("td")

        # if len(td_items) != 2:
        #     continue

        # Если пустой или None
        if not td_items:
            continue

        # Отбрасываем строки с годом, но без игры
        if len(td_items) == 1 and td_items[0].i is None:
            continue

        if len(td_items) == 2:
            year = td_items[0].text.strip()
            name = td_items[1].i.text.strip()

        else:
            # Сюда попадают игры, попавшие с другими в один и тот же год, например
            #     2000: Resident Evil Survivor
            #     2000: Resident Evil – Code: Veronica
            #
            # year берется из предыдущей строки
            # year = ...
            name = td_items[0].i.text.strip()

        if not is_match_row_func(tr):
            continue

        if year and name:
            items.append((year, name))

    return items
