#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List
from get_all_games import get_all_games


def get_games() -> List[str]:
    prefix = "Sable Maze".upper()
    postfix = "Collector's Edition".upper()

    return get_all_games(prefix=prefix, postfix=postfix)


if __name__ == '__main__':
    games = get_games()
    print(f'Games ({len(games)}):')

    for game in games:
        print('    ' + game)

