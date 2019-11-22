#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple

from bs4 import BeautifulSoup
import requests

from common import smart_comparing_names


def search_game_genres(game_name: str) -> List[Tuple[str, List[str]]]:
    rs = requests.get('https://gameguru.ru/search/all.html?s=' + game_name)
    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    for game in root.select('.jointCard-result-game-unit'):
        title = game.select_one('.jointCard-result-game-list-title').get_text(strip=True)
        genres = [a.get_text(strip=True) for a in game.select('a') if '/genre/' in a['href']]
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
    for name in [
        'Hellgate: London',
        'The Incredible Adventures of Van Helsing',
        'Dark Souls: Prepare to Die Edition',
        'Twin Sector',
        'Call of Cthulhu: Dark Corners of the Earth',
    ]:
        items = search_game_genres(name)
        print(f'Items ({len(items)}:')
        for game, genres in items:
            print(f'    {game!r}: {genres}')
        print()
        print(f'Genres of {name!r}: {get_game_genres(name)}')

        print('\n' + '-' * 20 + '\n')
