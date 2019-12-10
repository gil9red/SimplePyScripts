#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from typing import List

from bs4 import BeautifulSoup
import requests

from common import smart_comparing_names, USER_AGENT, get_norm_text


def get_game_genres(game_name: str, need_logs=False) -> List[str]:
    need_logs and print(f'[+] Search {game_name!r}...')

    headers = {
        'User-Agent': USER_AGENT,
    }

    session = requests.session()
    session.headers.update(headers)

    url = f'https://gamefaqs.gamespot.com/search?game={game_name}'
    rs = session.get(url)
    if not rs.ok:
        need_logs and print(f'  [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    for game_block_preview in root.select('.search_results_title > .search_result'):
        a = game_block_preview.select_one('.sr_name > a.log_search')
        title = get_norm_text(a)

        if not smart_comparing_names(title, game_name):
            continue

        url_game = urljoin(rs.url, a['href'])
        need_logs and print(f'  [+] Load {url_game!r}')

        rs = session.get(url_game)
        if not rs.ok:
            need_logs and print(f'    [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
            continue

        game_block = BeautifulSoup(rs.content, 'html.parser')
        game_info = game_block.select_one('.pod_gameinfo_left')
        if not game_info:
            return []

        # <li><b>Genre:</b>
        # <a href="/pc/category/54-action">Action</a> »
        # <a href="/pc/category/55-action-shooter">Shooter</a> »
        # <a href="/pc/category/80-action-shooter-third-person">Third-Person</a> »
        # <a href="/pc/category/182-action-shooter-third-person-arcade">Arcade</a>
        # </li>
        genres = [
            get_norm_text(a)
            for a in game_info.select_one('li > b:contains("Genre:")').find_next_siblings('a')
        ]

        # Сойдет первый, совпадающий по имени, вариант
        return genres

    return []


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Role-Playing', 'Western-Style']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Role-Playing', 'Action RPG']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['Role-Playing', 'Action RPG']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Action Adventure', 'Linear']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Action Adventure', 'Survival']
