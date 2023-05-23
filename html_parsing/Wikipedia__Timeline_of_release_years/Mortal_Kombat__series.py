#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Mortal_Kombat"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 1992: Mortal Kombat
# 1993: Mortal Kombat II
# 1995: Mortal Kombat 3
# 1995: Ultimate Mortal Kombat 3
# 1996: Mortal Kombat Trilogy
# 1997: Mortal Kombat Mythologies: Sub-Zero
# 1997: Mortal Kombat 4
# 1999: Mortal Kombat Gold
# 2000: Mortal Kombat: Special Forces
# 2002: Mortal Kombat: Deadly Alliance
# 2004: Mortal Kombat: Deception
# 2005: Mortal Kombat: Shaolin Monks
# 2006: Mortal Kombat: Armageddon
# 2006: Mortal Kombat: Unchained
# 2007: Ultimate Mortal Kombat
# 2008: Mortal Kombat vs. DC Universe
# 2011: Mortal Kombat
# 2011: Mortal Kombat Arcade Kollection
# 2012: Mortal Kombat: Komplete Edition
# 2015: Mortal Kombat X
# 2016: Mortal Kombat XL
# 2019: Mortal Kombat 11
