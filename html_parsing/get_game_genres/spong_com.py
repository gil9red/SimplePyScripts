#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from typing import List, Tuple

from bs4 import BeautifulSoup
import requests

from common import smart_comparing_names





def search_game_genres(game_name: str) -> List[Tuple[str, List[str]]]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    }

    url = f'https://spong.com/search/index.jsp?q={game_name}'
    rs = requests.get(url, headers=headers)
    if not rs.ok:
        print(f'[-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    # Первая таблица -- та, что нужна нам
    for game_block in root.select_one('table.searchResult').select('tr'):
        tds = game_block.select('td')

        # Например, tr > th
        if len(tds) != 4:
            continue

        td_title, _, genres_td, platforms_td = tds

        # Если игра не была на PC
        if not any('PC' in a.text.upper() for a in platforms_td.select('a')):
            continue

        # <td>Adventure: Free Roaming<br/>Adventure: Survival Horror<br/></td>
        #   -> ['Adventure: Free Roaming', 'Adventure: Survival Horror']
        genres = list(genres_td.stripped_strings)
        if not genres:
            continue

        title = td_title.a.get_text(strip=True)
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
    #   Result (8):
    #     'Hellgate: London': ['Adventure: Survival Horror']
    #     'London Racer': ['Racing: Car']
    #     'London Taxi Rushour': ['Racing: Car']
    #     'London Racer 2': ['Racing: Car']
    #     'London Underground Simulator: World of Subways 3': ['Simulation']
    #     'London Racer: World Challenge': ['Racing']
    #     'London 2012: The Official Video Game of the Olympic Games': ['Sport: Athletics']
    #     'Werewolves of London': ["Beat 'Em Up"]
    #
    # Genres: ['Adventure: Survival Horror']
    #
    # --------------------
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #   Result (2):
    #     'The Incredible Adventures of Van Helsing': ['Adventure: Role Playing']
    #     'The Adventures Of Tintin: The Secret of the Unicorn The Game': ['Adventure']
    #
    # Genres: ['Adventure: Role Playing']
    #
    # --------------------
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #   Result (7):
    #     'Dark Souls: Prepare to Die Edition': ['Adventure: Role Playing']
    #     'Dark Souls III: The Fire Fades Edition': ['Compilation', 'Adventure: Role Playing']
    #     'Dark Souls II: Scholar of the First Sin': ['Adventure: Role Playing', 'Compilation']
    #     "Dark Parables: The Red Riding Hood Sisters: Collector's Edition": ['Puzzle: Hidden Object']
    #     "Dark Tales 2: Edgar Allan Poe's The Black Cat Collector's Edition": ['Puzzle: Hidden Object']
    #     'Dark Parables 2: The Exiled Price Collector’s Edition': ['Puzzle: Hidden Object']
    #     'Dark Parables: Rise of the Snow Queen': ['Puzzle: Hidden Object']
    #
    # Genres: ['Adventure: Role Playing']
    #
    # --------------------
    #
    # Search 'Twin Sector'...
    #   Result (3):
    #     "Tony Hawk's Pro Skater 2": ['Sport: Skateboard']
    #     "Mat Hoffman's Pro BMX and Tony Hawk's Pro Skater 2 Twin Pack": ['Sport: Skateboard', 'Sport: Cycling']
    #     "Tony Hawk's Pro Skater 3": ['Sport: Skateboard']
    #
    # Genres: []
    #
    # --------------------
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #   Result (8):
    #     'Call of Cthulhu: Dark Corners of the Earth': ['Adventure: Survival Horror']
    #     'Call of Cthulhu: Beyond the Mountains of Madness': ['Adventure']
    #     'Call of Cthulhu: Destiny’s End': ['Adventure']
    #     'The Lord of the Rings The Battle for Middle-Earth II: The Rise of the Witch-King': ['Add-on pack', 'Strategy: Combat']
    #     'Robert D. Anderson & Das Erbe Cthulhus': ['Adventure: Survival Horror']
    #     'The Lord of the Rings: The Battle for Middle-Earth': ['Strategy: Combat']
    #     'Empire Earth II: The Art of Supremacy': ['Add-on pack', 'Strategy: Combat']
    #     'Defenders of the Earth': ['Platform', "Shoot 'Em Up"]
    #
    # Genres: ['Adventure: Survival Horror']
    #
    # --------------------
