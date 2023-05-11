#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/tarvitz/dsfp
import dsfp


# C:\Users\<CURRENT_USER>\Documents\NBGI\DarkSouls\<PLAYER_NAME>\DRAKS0005.sl2
file_name = "../print__deaths_from_save_file/DRAKS0005.sl2"

ds = dsfp.DSSaveFileParser(file_name)

stats_list = ds.get_stats()
print(f"Stats list ({len(stats_list)}): {stats_list}")
print()

print(f"Character ({len(stats_list)}):")

for stats in stats_list:
    name, deaths = stats["name"], stats["deaths"]
    print(f"    {name}, deaths: {deaths}")
