#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple

from bs4 import BeautifulSoup
import requests


def get_games() -> List[Tuple[str, str]]:
    rs = requests.get('https://yuzu-emu.org/game/')
    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    for tr in root.select('table')[1].select('tr'):
        tds = tr.select('td')
        if len(tds) != 3:
            continue

        td_title, td_compatibility, _ = tds
        items.append((
            td_title.get_text(strip=True),
            td_compatibility.get_text(strip=True)
        ))

    return items


if __name__ == '__main__':
    games = get_games()
    print('Total:', len(games))
    # Total: 1145

    print()

    print("Total perfect + great:", len([x for x in games if x[1] in ('Perfect', 'Great')]))
    # Total perfect + great: 301

    print()

    perfect_games = [x for x in games if x[1] == 'Perfect']
    print(f'Total perfect({len(perfect_games)}):')
    for i, (game, _) in enumerate(perfect_games, 1):
        print(f'{i}. {game}')

    # Total perfect(101):
    # ...
