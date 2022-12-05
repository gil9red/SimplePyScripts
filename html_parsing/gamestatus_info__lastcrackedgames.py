#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests


session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'


def get_games() -> list[str]:
    rs = session.get('https://gamestatus.info/back/api/gameinfo/game/lastcrackedgames/')
    rs.raise_for_status()

    return [game['title'] for game in rs.json()['list_crack_games']]


if __name__ == '__main__':
    items = get_games()
    print(f'Games ({len(items)}): {items}')
    # Games (200): ['The Knight Witch', ..., 'Rogue Lords']
