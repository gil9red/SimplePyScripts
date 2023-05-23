#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Angry_Birds"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 2009: Angry Birds
# 2010: Seasons
# 2011: Rio
# 2012: Friends
# 2012: Space
# 2012: Star Wars
# 2013: Star Wars II
# 2013: Go!
# 2014: Epic
# 2014: Transformers
# 2015: Flight!
# 2015: 2
# 2016: Action!
# 2016: Blast!
# 2017: Evolution
# 2017: Match
# 2018: Blast Island
# 2018: Dream Blast
# 2019: Isle of Pigs
