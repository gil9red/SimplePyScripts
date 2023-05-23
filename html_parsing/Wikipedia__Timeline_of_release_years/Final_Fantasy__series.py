#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Final_Fantasy"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 1987: Final Fantasy
# 1988: Final Fantasy II
# 1990: Final Fantasy III
# 1991: Final Fantasy IV
# 1992: Final Fantasy V
# 1994: Final Fantasy VI
# 1997: Final Fantasy VII
# 1999: Final Fantasy VIII
# 2000: Final Fantasy IX
# 2001: Final Fantasy X
# 2002: Final Fantasy XI
# 2006: Final Fantasy XII
# 2009: Final Fantasy XIII
# 2010: Final Fantasy XIV
# 2016: Final Fantasy XV
