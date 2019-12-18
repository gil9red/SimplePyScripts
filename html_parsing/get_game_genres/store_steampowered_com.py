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

    # category1 = Игры
    url = f'https://store.steampowered.com/search/?term={game_name}&category1=998'
    rs = session.get(url)
    if not rs.ok:
        need_logs and print(f'  [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    for game_block_preview in root.select('.search_result_row'):
        title = get_norm_text(game_block_preview.select_one('.search_name > .title'))
        if not smart_comparing_names(title, game_name):
            continue

        href = game_block_preview['href']
        url_game = urljoin(rs.url, href)
        need_logs and print(f'  [+] Load {url_game!r}')

        rs = session.get(url_game)
        if not rs.ok:
            need_logs and print(f'    [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
            continue

        game_block = BeautifulSoup(rs.content, 'html.parser')
        # <div class="details_block">
        #     <b>Title:</b> HELLGATE: London<br>
        #     <b>Genre:</b>
        #     <a href="https://store.steampowered.com/genre/Action/?snr=1_5_9__408">Action</a>,
        #     <a href="https://store.steampowered.com/genre/RPG/?snr=1_5_9__408">RPG</a>
        genres = [
            get_norm_text(a) for a in game_block.select('.details_block > a[href*="/genre/"]')
        ]

        # Сойдет первый, совпадающий по имени, вариант
        return genres

    return []


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Action', 'RPG']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Action', 'Adventure', 'Indie', 'RPG']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['Action', 'RPG']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Action', 'Adventure']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: []
