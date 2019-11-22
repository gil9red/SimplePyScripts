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

    rs = requests.get(f'https://gameguru.ru/search/all.html?s={game_name}', headers=headers)
    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    for game_block in root.select('.jointCard-result-game-unit'):
        title = game_block.select_one('.jointCard-result-game-list-title').get_text(strip=True)
        genres = [a.get_text(strip=True) for a in game_block.select('a') if '/genre/' in a['href']]
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
    #   Result (3):
    #     'Hellgate: London': ['RPG']
    #     'London Detective Mysteria': ['Квест', 'Визуальный роман']
    #     'Mario & Sonic at the London 2012 Olympic Games': ['Спорт']
    #
    # Genres: ['RPG']
    #
    # --------------------
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #   Result (3):
    #     'Incredible Adventures of Van Helsing, The': ['Экшен', 'RPG']
    #     'Incredible Adventures of Van Helsing 2, The': ['Экшен', 'RPG']
    #     'Incredible Adventures of Van Helsing: Final Cut, The': ['Экшен', 'RPG']
    #
    # Genres: ['Экшен', 'RPG']
    #
    # --------------------
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #   Result (3):
    #     'Dark Souls: Prepare to Die Edition': ['RPG', 'aRPG']
    #     'Dark Age of Camelot Platinum Edition': ['RPG', 'MMO']
    #     'Dark Age of Camelot: Gold Edition': ['RPG', 'MMO']
    #
    # Genres: ['RPG', 'aRPG']
    #
    # --------------------
    #
    # Search 'Twin Sector'...
    #   Result (3):
    #     'Twin Sector': ['Экшен']
    #     'Twin Mirror': ['Квест']
    #     'Aragami': ['Экшен', 'Стелс']
    #
    # Genres: ['Экшен']
    #
    # --------------------
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #   Result (3):
    #     'Call of Cthulhu: Dark Corners of the Earth': ['Экшен', 'Шутер', 'Квест']
    #     'Call of Cthulhu': ['RPG']
    #     'Call of Cthulhu: The Wasted Land': ['RPG', 'Стратегия']
    #
    # Genres: ['Экшен', 'Шутер', 'Квест']
    #
    # --------------------
