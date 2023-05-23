#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Metal_Gear"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 1987: Metal Gear
# 1990: Snake's Revenge
# 1990: Metal Gear 2: Solid Snake
# 1998: Metal Gear Solid
# 2000: Metal Gear: Ghost Babel
# 2001: Metal Gear Solid 2: Sons of Liberty
# 2004: Metal Gear Solid: The Twin Snakes
# 2004: Metal Gear Solid 3: Snake Eater
# 2004: Metal Gear Acid
# 2005: Metal Gear Acid 2
# 2006: Metal Gear Solid: Portable Ops
# 2007: Metal Gear Solid: Portable Ops Plus
# 2008: Metal Gear Solid Mobile
# 2008: Metal Gear Solid 4: Guns of the Patriots
# 2010: Metal Gear Solid: Peace Walker
# 2013: Metal Gear Rising: Revengeance
# 2014: Metal Gear Solid V: Ground Zeroes
# 2015: Metal Gear Solid V: The Phantom Pain
# 2018: Metal Gear Survive
