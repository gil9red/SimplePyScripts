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
        'mode': '11',
        's': '1',
        'p': '1',
        'fg': 'all',
        'fp': 'pc',
        'fn': game_name
    }

    url = 'https://www.igromania.ru/-Engine-/AJAX/games.list.v2/index.php'
    rs = requests.post(url, headers=headers, data=form_data)
    if not rs.ok:
        print(f'[-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    for game_block in root.select('.gamebase_box'):
        # Символ "\xa0" появится, если среди тегов будет "&nbsp;"
        title = game_block.select_one('.release_name').get_text(strip=True).replace('\xa0', ' ')
        genres = [a.get_text(strip=True) for a in game_block.select('.genre > a')]
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
    #     'Hellgate: London': ['Боевик', 'Боевик от первого лица', 'Боевик от третьего лица', 'Ролевая игра']
    #
    # Genres: ['Боевик', 'Боевик от первого лица', 'Боевик от третьего лица', 'Ролевая игра']
    #
    # --------------------
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #   Result (4):
    #     'The Incredible Adventures of Van Helsing': ['Ролевая игра', 'Боевик', 'Боевик от третьего лица']
    #     'The Incredible Adventures of Van Helsing 2': ['Ролевая игра', 'Боевик', 'Боевик от третьего лица']
    #     'The Incredible Adventures of Van Helsing III': ['Ролевая игра', 'Боевик', 'Боевик от третьего лица']
    #     'The Incredible Adventures of Van Helsing: Arcane Mechanic': ['Ролевая игра', 'Боевик', 'Боевик от третьего лица']
    #
    # Genres: ['Ролевая игра', 'Боевик', 'Боевик от третьего лица']
    #
    # --------------------
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #   Result (0):
    #
    # Genres: []
    #
    # --------------------
    #
    # Search 'Twin Sector'...
    #   Result (1):
    #     'Twin Sector': ['Боевик', 'Боевик от первого лица']
    #
    # Genres: ['Боевик', 'Боевик от первого лица']
    #
    # --------------------
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #   Result (1):
    #     'Call of Cthulhu: Dark Corners of the Earth': ['Боевик', 'Ужасы', 'Боевик от первого лица', 'Приключение']
    #
    # Genres: ['Боевик', 'Ужасы', 'Боевик от первого лица', 'Приключение']
    #
    # --------------------
