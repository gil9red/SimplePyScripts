#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASES" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/Grand_Theft_Auto"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 1997: Grand Theft Auto
# 1999: Grand Theft Auto: London 1969
# 1999: Grand Theft Auto: London 1961
# 1999: Grand Theft Auto 2
# 2001: Grand Theft Auto III
# 2002: Grand Theft Auto: Vice City
# 2004: Grand Theft Auto: San Andreas
# 2004: Grand Theft Auto: Advance
# 2005: Grand Theft Auto: Liberty City Stories
# 2006: Grand Theft Auto: Vice City Stories
# 2008: Grand Theft Auto IV
# 2009: Grand Theft Auto IV: The Lost and Damned
# 2009: Grand Theft Auto: Chinatown Wars
# 2009: Grand Theft Auto: The Ballad of Gay Tony
# 2013: Grand Theft Auto V
