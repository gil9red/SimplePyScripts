#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


def is_match_row_func(tr) -> bool:
    td_items = tr.select("td")
    td = td_items[0] if len(td_items) == 1 else td_items[1]

    # Check <b>. Because "Main series in bold"
    return td.i.b is not None


url = "https://en.wikipedia.org/wiki/The_Elder_Scrolls"
for year, name in get_parsed_two_column_wikitable(
    url, is_match_table_func, is_match_row_func
):
    print(f"{year}: {name}")

# 1994: The Elder Scrolls: Arena
# 1996: The Elder Scrolls II: Daggerfall
# 2002: The Elder Scrolls III: Morrowind
# 2006: The Elder Scrolls IV: Oblivion
# 2011: The Elder Scrolls V: Skyrim
# TBA: The Elder Scrolls VI
