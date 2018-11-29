#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
sys.path.append('..')

from common import find_locations_ds3, find_links_ds3


visited_locations, links = find_locations_ds3()

# Выведем итоговый список
print(len(visited_locations), visited_locations)
print(len(links), links)

print()

links = find_links_ds3(log=False)
print(len(links), links)
