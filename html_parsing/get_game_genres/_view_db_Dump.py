#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from db import Dump


print('Total:', Dump.select().count())

genres = Dump.get_all_genres()
print(f'Genres ({len(genres)}): {genres}')

games = Dump.get_all_games()
print(f'Games ({len(games)}): {games}')

sites = Dump.get_all_sites()
print(f'Sites ({len(sites)}): {sites}')

print()

max_width = max(len(x.site) for x in Dump.select(Dump.site).distinct())
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
