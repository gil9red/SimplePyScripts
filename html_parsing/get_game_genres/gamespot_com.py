#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from typing import List, Tuple
import time

from bs4 import BeautifulSoup
import requests

from common import smart_comparing_names


_CACHE__GAME_GENRES = dict()

# Ссылки из этого кеша не будем грузить
_CACHE__NO_LOAD = []


def search_game_genres(game_name: str) -> List[Tuple[str, List[str]]]:
    print(f'[+] Search {game_name!r}...')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    }

    session = requests.session()
    session.headers.update(headers)

    url = f'https://www.gamespot.com/search/?i=site&q={game_name}'
    rs = session.get(url)
    if not rs.ok:
        print(f'  [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    for game_block_preview in root.select('.media-body'):
        if not game_block_preview.select_one('.media-date'):
            continue

        href = game_block_preview.select_one('.media-title a')['href']
        url_game = urljoin(rs.url, href)
        if url_game in _CACHE__GAME_GENRES:
            cache = _CACHE__GAME_GENRES[url_game]
            items.append(cache)
            print(f'  [+] Found cache of {url_game!r}, skip load. Cache: {cache}')
            continue

        if url_game in _CACHE__NO_LOAD:
            print(f'  [+] Found cache unnecessary of {url_game!r}, skip load.')
            continue

        print(f'  [+] Load {url_game!r}')

        rs = session.get(url_game)
        if not rs.ok:
            print(f'    [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
            continue

        game_block = BeautifulSoup(rs.content, 'html.parser')

        tag_system_list = game_block.select_one('.gameObject__description .system-list')
        tag_title = game_block.select_one('.gameObject__title')
        tag_object_stats = game_block.select_one('#object-stats-wrap')

        if not tag_title or not tag_system_list or not tag_object_stats:
            print('    [-] Added url in _CACHE__NO_LOAD. Reason: missing tag_system_list or tag_title '
                  'or tag_object_stats')
            _CACHE__NO_LOAD.append(url_game)
            continue

        if 'PC' not in tag_system_list.get_text(strip=True).upper():
            print('    [-] Added url in _CACHE__NO_LOAD. Reason: no PC')
            _CACHE__NO_LOAD.append(url_game)
            continue

        genres = [a.get_text(strip=True) for a in tag_object_stats.select('a[href]') if '/genre/' in a['href']]
        if not genres:
            print('    [-] Added url in _CACHE__NO_LOAD. Reason: genres is empty')
            _CACHE__NO_LOAD.append(url_game)
            continue

        title = tag_title.get_text(strip=True)
        items.append(
            (title, genres)
        )
        _CACHE__GAME_GENRES[url_game] = (title, genres)

        time.sleep(1)

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
    #   Result (4):
    #     'Hellgate: London': ['Role-Playing']
    #     'Hellgate (2011)': ['MMO', 'Role-Playing']
    #     'Hellgate: Tokyo': ['MMO', 'Role-Playing']
    #     'Werewolves of London': ['Action']
    #
    # Genres: ['Role-Playing']
    #
    # --------------------
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #   Result (7):
    #     'The Incredible Adventures of Van Helsing': ['Action', 'Role-Playing']
    #     'The Incredible Adventures of Van Helsing II': ['Action', 'Role-Playing']
    #     'The Incredible Adventures of Van Helsing III': ['Action', 'Role-Playing']
    #     'World of Van Helsing: Deathtrap': ['Strategy']
    #     'The Incredible Adventures of Super Panda': ['2D', 'Action', 'Platformer']
    #     'Incredible Adventures of my Mom': ['Puzzle']
    #     'BVRGER VAN': ['Simulation', 'VR']
    #
    # Genres: ['Action', 'Role-Playing']
    #
    # --------------------
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #   Result (9):
    #     'Dark Souls II': ['Role-Playing', 'Action']
    #     'Dark Souls III': ['Action', 'Role-Playing']
    #     'Dark Souls': ['Action', 'Role-Playing']
    #     'Sekiro: Shadows Die Twice': ['Action', 'Adventure']
    #     'Die In The Dark': ['Action', 'Adventure', 'Survival', '3D']
    #     'Dark Romance: A Performance to Die For': ['Puzzle', 'Hidden Object']
    #     "D4: Dark Dreams Don't Die": ['Adventure']
    #     'Teleglitch: Die More Edition': ['Action', 'Fixed-Screen', 'Shooter', '2D']
    #     'Dark Fall 3: Lost Souls': ['Adventure', 'First-Person', '3D']
    #
    # Genres: []
    #
    # --------------------
    #
    # Search 'Twin Sector'...
    #   Result (10):
    #     'Twin Sector': ['Action', 'Adventure']
    #     'SECTOR': ['First-Person', 'Shooter', '3D', 'Action']
    #     'Dark Sector': ['Shooter', 'Third-Person', '3D', 'Action']
    #     '7th Sector': ['Adventure']
    #     'Identity Sector': ['Strategy']
    #     'Chaos Sector': ['Strategy', 'Turn-Based']
    #     'Hostile Sector': ['Strategy', 'Turn-Based']
    #     'G-Sector': ['Action']
    #     'Sector 724': ['Strategy', 'Turn-Based']
    #     'Turret Sector': ['Real-Time', 'Strategy']
    #
    # Genres: ['Action', 'Adventure']
    #
    # --------------------
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #   Result (9):
    #     'Call of Cthulhu: Dark Corners of the Earth': ['3D', 'Action', 'Adventure', 'Survival']
    #     'Call of Duty: Modern Warfare': ['Action', 'First-Person', 'Shooter', '3D']
    #     'Call of Cthulhu: The Official Video Game': ['Role-Playing']
    #     'Call of Cthulhu: The Wasted Land': ['Strategy', 'Turn-Based']
    #     'Dark Earth': ['Action', 'Adventure']
    #     'Call of Cthulhu: Shadow of the Comet': ['Adventure']
    #     "Asheron's Call Dark Majesty": ['MMO', 'Role-Playing']
    #     'Middle-earth: Shadow of War': ['Action', 'Adventure']
    #     'Odallus: The Dark Call': ['Adventure', 'Action']
    #
    # Genres: ['3D', 'Action', 'Adventure', 'Survival']
    #
    # --------------------
