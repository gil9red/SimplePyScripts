#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

from bs4 import BeautifulSoup
import requests

from common import smart_comparing_names, USER_AGENT, get_norm_text, get_uniques


def get_game_genres(game_name: str, need_logs=False) -> List[str]:
    headers = {
        'User-Agent': USER_AGENT,
    }

    rs = requests.get(f'https://gameguru.ru/search/all.html?s={game_name}', headers=headers)
    if not rs.ok:
        need_logs and print(f'[-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    for game_block in root.select('.jointCard-result-game-unit'):
        title = get_norm_text(game_block.select_one('.jointCard-result-game-list-title'))
        if not smart_comparing_names(title, game_name):
            continue

        genres = [get_norm_text(a) for a in game_block.select('a') if '/genre/' in a['href']]

        # Сойдет первый, совпадающий по имени, вариант
        return get_uniques(genres)

    return []


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['RPG']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Экшен', 'RPG']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['RPG', 'aRPG']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Экшен']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Экшен', 'Шутер', 'Квест']
