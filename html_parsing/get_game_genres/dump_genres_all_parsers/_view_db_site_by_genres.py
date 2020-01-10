#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from db import Dump


genres = Dump.get_all_genres()
print(f'Genres ({len(genres)}): {genres}')

sites = Dump.get_all_sites()
print(f'Sites ({len(sites)}): {sites}')

print()

max_width = max(len(x.site) for x in Dump.select(Dump.site).distinct())
fmt_str = '{:<%d} : ({}) {}' % max_width

site_by_genres = defaultdict(list)
for x in Dump.get():
    site_by_genres[x.site] += x.genres

for k, v in site_by_genres.items():
    site_by_genres[k] = sorted(set(v))

print(f'Total {len(site_by_genres)}:')

for site, genres in site_by_genres.items():
    print(fmt_str.format(site, len(genres), genres))
