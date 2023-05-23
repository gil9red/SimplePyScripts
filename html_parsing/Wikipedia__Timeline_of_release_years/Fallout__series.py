#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Fallout_(series)"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 1997: Fallout
# 1998: Fallout 2
# 2001: Fallout Tactics: Brotherhood of Steel
# 2004: Fallout: Brotherhood of Steel
# 2008: Fallout 3
# 2010: Fallout: New Vegas
# 2015: Fallout Shelter
# 2015: Fallout 4
# 2018: Fallout 76
