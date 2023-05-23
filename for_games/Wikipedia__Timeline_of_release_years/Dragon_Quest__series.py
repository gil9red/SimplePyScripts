#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Dragon_Quest"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 1986: Dragon Quest
# 1987: Dragon Quest II
# 1988: Dragon Quest III
# 1990: Dragon Quest IV
# 1992: Dragon Quest V
# 1995: Dragon Quest VI
# 2000: Dragon Quest VII
# 2004: Dragon Quest VIII
# 2009: Dragon Quest IX
# 2012: Dragon Quest X
# 2017: Dragon Quest XI
