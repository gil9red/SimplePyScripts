#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
sys.path.append('..')

from common import parse_locations_ds1, find_links_ds1


visited_locations, links, bosses = parse_locations_ds1()

# Выведем итоговый список
print(len(visited_locations), visited_locations)
print(len(links), links)
print(len(bosses), bosses)

print()

links = find_links_ds1(log=False)
print(len(links), links)
