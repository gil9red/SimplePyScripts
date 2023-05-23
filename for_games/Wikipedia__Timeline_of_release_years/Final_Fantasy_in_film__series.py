#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "FINAL FANTASY IN FILM" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Final_Fantasy"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 1994: Final Fantasy: Legend of the Crystals
# 2001: Final Fantasy: The Spirits Within
# 2001: Final Fantasy: Unlimited
# 2005: Final Fantasy VII: Advent Children
# 2005: Last Order: Final Fantasy VII
# 2016: Kingsglaive: Final Fantasy XV
# 2016: Brotherhood: Final Fantasy XV
