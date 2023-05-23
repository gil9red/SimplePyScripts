#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_table_func(table) -> bool:
    return "TIMELINE OF RELEASE YEARS" in table.caption.text.strip().upper()


url = "https://en.wikipedia.org/wiki/The_Elder_Scrolls"
for year, name in get_parsed_two_column_wikitable(url, is_match_table_func):
    print(f"{year}: {name}")

# 1994: The Elder Scrolls: Arena
# 1996: The Elder Scrolls II: Daggerfall
# 1997: An Elder Scrolls Legend: Battlespire
# 1998: The Elder Scrolls Adventures: Redguard
# 2002: The Elder Scrolls III: Morrowind
# 2002: The Elder Scrolls III: Tribunal
# 2003: The Elder Scrolls III: Bloodmoon
# 2003: The Elder Scrolls Travels: Stormhold
# 2004: The Elder Scrolls Travels: Dawnstar
# 2004: The Elder Scrolls Travels: Shadowkey
# 2006: The Elder Scrolls IV: Oblivion
# 2006: The Elder Scrolls IV: Knights of the Nine
# 2007: The Elder Scrolls IV: Shivering Isles
# 2011: The Elder Scrolls V: Skyrim
# 2012: The Elder Scrolls V: Skyrim – Dawnguard
# 2012: The Elder Scrolls V: Skyrim – Hearthfire
# 2012: The Elder Scrolls V: Skyrim – Dragonborn
# 2014: The Elder Scrolls Online
# 2016: The Elder Scrolls V: Skyrim – Special Edition
# 2017: The Elder Scrolls: Legends
# 2017: The Elder Scrolls: Skyrim - VR
# 2017: The Elder Scrolls Online - Morrowind
# 2018: The Elder Scrolls Online - Summerset
# 2019: The Elder Scrolls: Blades
# 2019: The Elder Scrolls Online - Elsweyr
# TBA: The Elder Scrolls VI
