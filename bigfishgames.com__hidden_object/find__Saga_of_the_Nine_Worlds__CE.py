#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


PREFIX = "Saga of the Nine Worlds".upper()
POSTFIX = "Collector's Edition".upper()

from get_all_games import get_all_games
games = [game for game in get_all_games() if game.upper().startswith(PREFIX) and game.upper().endswith(POSTFIX)]
print('Games ({}):'.format(len(games)))

for game in games:
    print('    ' + game)
