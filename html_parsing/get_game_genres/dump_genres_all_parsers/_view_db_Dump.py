#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from db import Dump


sites = [x.site for x in Dump.select(Dump.site).distinct()]
max_width = len(max(sites, key=len))
fmt_str = '    {:<%d} : {}' % max_width

game_by_dump = defaultdict(list)
for x in Dump.get():
    game_by_dump[x.name].append(x)

for game, dumps in game_by_dump.items():
    print(game)

    for dump in dumps:
        print(
            fmt_str.format(dump.site, dump.genres)
        )

    print()
