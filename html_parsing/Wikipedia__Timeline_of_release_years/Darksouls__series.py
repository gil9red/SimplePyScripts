#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Souls_(series)"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 2009: Demon's Souls
# 2011: Dark Souls
# 2014: Dark Souls II
# 2015: Dark Souls II: Scholar of the First Sin
# 2016: Dark Souls III
# 2018: Dark Souls: Remastered
