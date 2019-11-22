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
        'X-Requested-With': 'XMLHttpRequest',
    }
    form_data = {
        'search-query': game_name,
        'search-obl': 'games',
        'page': '1',
    }

    rs = requests.post('https://gamer-info.com/search-q/', headers=headers, data=form_data)
    if not rs.ok:
        print(f'[-] rs.ok={rs.ok}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    for game_block in root.select('.games > .c2'):
        g = game_block.select_one('.g')
        if 'Жанр:' not in g.text:
            continue

        title = game_block.select_one('.n').get_text(strip=True)
        genres = g.text.replace('Жанр:', '').strip().split(', ')

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
    #     'Hellgate: London': ['action', 'RPG']
    #
    # Genres: ['action', 'RPG']
    #
    # --------------------
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #   Result (4):
    #     'The Incredible Adventures of Van Helsing (Ван Хельсинг. Новая история)': ['hack & slash']
    #     'The Incredible Adventures of Van Helsing II (Van Helsing 2. Смерти вопреки)': ['hack & slash']
    #     'The Incredible Adventures of Van Helsing: Final Cut': ['hack & slash']
    #     'The Incredible Adventures of Van Helsing III': ['hack & slash']
    #
    # Genres: []
    #
    # --------------------
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #   Result (1):
    #     'Dark Souls': ['action', 'RPG']
    #
    # Genres: []
    #
    # --------------------
    #
    # Search 'Twin Sector'...
    #   Result (1):
    #     'Twin Sector': ['action', 'приключения']
    #
    # Genres: ['action', 'приключения']
    #
    # --------------------
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #   Result (1):
    #     'Call of Cthulhu: Dark Corners of the Earth': ['action', 'приключения']
    #
    # Genres: ['action', 'приключения']
    #
    # --------------------
