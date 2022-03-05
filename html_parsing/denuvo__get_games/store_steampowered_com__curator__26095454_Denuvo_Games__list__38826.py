#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Games that had Denuvo removed
"""


import json

import requests
from bs4 import BeautifulSoup


session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'


def get_games() -> list[str]:
    rs = session.get('https://store.steampowered.com/curator/26095454-Denuvo-Games/list/38826/')
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, 'html.parser')

    data_applinkinfo: list = json.loads(
        root.select_one('#application_config')['data-applinkinfo']
    )
    items = [game['title'] for game in data_applinkinfo]
    items.sort()
    return items


if __name__ == '__main__':
    games = get_games()
    print(f'Total games ({len(games)}): {games[0]!r} - {games[-1]!r}')
    # Total games (63): '2Dark' - 'Yakuza 0'
