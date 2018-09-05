#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import typing
from get_all_games import get_all_games


def get_games() -> typing.List[str]:
    prefix = "Saga of the Nine Worlds"
    postfix = "Collector's Edition"

    return get_all_games(prefix=prefix, postfix=postfix)


if __name__ == '__main__':
    games = get_games()
    print('Games ({}):'.format(len(games)))

    for game in games:
        print('    ' + game)
