#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
sys.path.append("..")

from common import Parser, find_bosses_of_location_ds2


p = Parser.DS2(log=False).parse()

for location in p.get_locations():
    print(f"{location} -> {p.get_location_by_url(location)}")

    for boss, url in p.get_location_by_bosses(location):
        print(f"   {boss} -> {url}")

    print()

print()

bosses_of_location = find_bosses_of_location_ds2()
print(len(bosses_of_location), bosses_of_location)
