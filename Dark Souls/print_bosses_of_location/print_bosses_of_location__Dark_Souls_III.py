#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
sys.path.append('..')

from common import parse_locations_ds3
from collections import defaultdict


visited_locations, links, bosses = parse_locations_ds3(log=False)

location_by_bosses = defaultdict(list)
for location, boss in bosses:
    location_by_bosses[location].append(boss)

for location in visited_locations:
    print(f'{location}:')
    for boss in location_by_bosses[location]:
        print(f'   {boss}')

    print()
