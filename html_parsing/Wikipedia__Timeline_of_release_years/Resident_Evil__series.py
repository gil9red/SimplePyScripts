#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Resident_Evil"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 1996: Resident Evil
# 1998: Resident Evil 2
# 1999: Resident Evil 3: Nemesis
# 2000: Resident Evil Survivor
# 2000: Resident Evil – Code: Veronica
# 2001: Resident Evil Gaiden
# 2001: Resident Evil Survivor 2 – Code: Veronica
# 2002: Resident Evil
# 2002: Resident Evil Zero
# 2003: Resident Evil: Dead Aim
# 2003: Resident Evil Outbreak
# 2004: Resident Evil Outbreak: File #2
# 2005: Resident Evil 4
# 2007: Resident Evil: The Umbrella Chronicles
# 2009: Resident Evil 5
# 2009: Resident Evil: The Darkside Chronicles
# 2011: Resident Evil: The Mercenaries 3D
# 2012: Resident Evil: Revelations
# 2012: Resident Evil: Operation Raccoon City
# 2012: Resident Evil 6
# 2015: Resident Evil: Revelations 2
# 2016: Umbrella Corps
# 2017: Resident Evil 7: Biohazard
# 2019: Resident Evil 2
