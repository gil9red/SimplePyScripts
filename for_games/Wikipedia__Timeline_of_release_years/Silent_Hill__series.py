#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Silent_Hill"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 1999: Silent Hill
# 2001: Play Novel: Silent Hill
# 2001: Silent Hill 2
# 2003: Silent Hill 3
# 2004: Silent Hill 4: The Room
# 2006: Silent Hill
# 2007: Silent Hill: The Arcade
# 2007: Silent Hill: Origins
# 2007: Silent Hill: Orphan
# 2007: Silent Hill: The Escape
# 2008: Silent Hill: Orphan 2
# 2008: Silent Hill: Homecoming
# 2009: Silent Hill: Shattered Memories
# 2010: Silent Hill: Orphan 3
# 2012: Silent Hill: Downpour
# 2012: Silent Hill HD Collection
# 2012: Silent Hill: Book of Memories
# 2014: P.T.
