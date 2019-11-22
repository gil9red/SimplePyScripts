#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple

from bs4 import BeautifulSoup
import requests

from common import smart_comparing_names


def search_game_genres(game_name: str) -> List[Tuple[str, List[str]]]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    }

    rs = requests.get(f'https://stopgame.ru/search/?s={game_name}&where=games&sort=name', headers=headers)
    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    for game_block in root.select('.game-block'):
        title = game_block.select_one('.title').get_text(strip=True)
        genres = [a.get_text(strip=True) for a in game_block.select('.game-genre-value > a') if '?genre[]' in a['href']]
        items.append(
            (title, genres)
        )

    return items


def get_game_genres(game_name: str) -> List[str]:
    for game, genres in search_game_genres(game_name):
        if smart_comparing_names(game, game_name):
            return genres

    return []


if __name__ == '__main__':
    from common import _common_test
    _common_test(search_game_genres, get_game_genres)

    # Search 'Hellgate: London'...
    #   Result (1):
    #     'Hellgate: London': ['action', 'rpg']
    #
    # Genres: ['action', 'rpg']
    #
    # --------------------
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #   Result (5):
    #     'Incredible Adventures of Van Helsing II, The': ['rpg']
    #     'Incredible Adventures of Van Helsing III, The': ['rpg']
    #     'Incredible Adventures of Van Helsing, The': ['rpg']
    #     'Incredible Adventures of Van Helsing: Arcane Mechanic, The': ['add-on', 'rpg']
    #     'Incredible Adventures of Van Helsing: Final Cut, The': ['rpg']
    #
    # Genres: ['rpg']
    #
    # --------------------
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #   Result (1):
    #     'Dark Souls': ['rpg']
    #
    # Genres: []
    #
    # --------------------
    #
    # Search 'Twin Sector'...
    #   Result (1):
    #     'Twin Sector': ['action', 'logic']
    #
    # Genres: ['action', 'logic']
    #
    # --------------------
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #   Result (1):
    #     'Call of Cthulhu: Dark Corners of the Earth': ['action', 'adventure']
    #
    # Genres: ['action', 'adventure']
    #
    # --------------------
