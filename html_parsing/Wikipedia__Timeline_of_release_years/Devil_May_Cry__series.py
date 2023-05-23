#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Devil_May_Cry"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 2001: Devil May Cry
# 2003: Devil May Cry 2
# 2005: Devil May Cry 3: Dante's Awakening
# 2008: Devil May Cry 4
# 2012: Devil May Cry HD Collection
# 2013: DmC: Devil May Cry
# 2019: Devil May Cry 5
