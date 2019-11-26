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

    url = f'https://iwantgames.ru/?s={game_name}'
    rs = requests.get(url, headers=headers)
    if not rs.ok:
        print(f'[-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    for game_block in root.select('.game__content'):
        # Если игра не была на PC
        if 'PC' not in game_block.select_one('.game__platforms').text.upper():
            continue

        # <dt>Жанр:</dt>
        # <dd>
        #     <a href="https://iwantgames.ru/rpg/">РПГ</a>,
        #     <a href="https://iwantgames.ru/horror/">Ужасы</a>,
        #     <a href="https://iwantgames.ru/action/">Экшен</a>
        # </dd>
        #   -> ['РПГ', 'Ужасы', 'Экшен']
        dt = game_block.find('dt', text='Жанр:')
        if not dt:
            continue

        dd = dt.find_next_sibling('dd')
        if not dd:
            continue

        genres = [a.get_text(strip=True) for a in dd.find_all('a')]
        title = game_block.h2.a.get_text(strip=True)
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
    #   Result (0):
    #
    # Genres: []
    #
    # --------------------
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #   Result (1):
    #     'The Incredible Adventures of Van Helsing: Final Cut': ['РПГ', 'Ужасы', 'Экшен']
    #
    # Genres: []
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
    #   Result (0):
    #
    # Genres: []
    #
    # --------------------
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #   Result (0):
    #
    # Genres: []
    #
    # --------------------

    name = 'Dark Souls: Remastered'
    print(get_game_genres(name))  # ['РПГ', 'Ужасы', 'Экшен']
