#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import find_locations_ds2, find_links_ds2


visited_locations, links = find_locations_ds2()

# Выведем итоговый список
print(len(visited_locations), visited_locations)
print(len(links), links)

print()

links = find_links_ds2(log=False)
print(len(links), links)
