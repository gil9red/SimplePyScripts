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


url = "https://en.wikipedia.org/wiki/Fallout_(series)"
for year, name in get_parsed_two_column_wikitable(
    url, is_match_table_func, is_match_row_func
):
    print(f"{year}: {name}")

# 1997: Fallout
# 1998: Fallout 2
# 2008: Fallout 3
# 2015: Fallout 4
