#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from typing import List

from bs4 import BeautifulSoup
import requests

from common import smart_comparing_names, USER_AGENT, get_norm_text, get_uniques, get_logger


log = get_logger(__file__)


def get_game_genres(game_name: str, need_logs=False) -> List[str]:
    need_logs and log.info(f'Search {game_name!r}...')

    headers = {
        'User-Agent': USER_AGENT,
    }

    session = requests.session()
    session.headers.update(headers)

    url = f'https://www.metacritic.com/search/game/{game_name}/results'
    rs = session.get(url)
    if not rs.ok:
        need_logs and log.warning(f'Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    for game_block_preview in root.select('.result'):
        a = game_block_preview.select_one('.product_title > a')
        title = get_norm_text(a)
        if not smart_comparing_names(title, game_name):
            continue

        url_game = urljoin(rs.url, a['href'])
        need_logs and log.info(f'Load {url_game!r}')

        rs = session.get(url_game)
        if not rs.ok:
            need_logs and log.warning(f'Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
            continue

        game_block = BeautifulSoup(rs.content, 'html.parser')
        # <li class="summary_detail product_genre">
        #     <span class="label">Genre(s): </span>
        #     <span class="data">Role-Playing</span>,
        #     <span class="data">Action RPG</span>
        # </li>
        genres = [
            get_norm_text(a) for a in game_block.select('.summary_detail.product_genre > .data')
        ]

        # Сойдет первый, совпадающий по имени, вариант
        genres = get_uniques(genres)

        need_logs and log.info(f'Genres: {genres}')
        return genres

    need_logs and log.info(f'Not found game {game_name!r}')
    return []


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Role-Playing', 'First-Person', 'First-Person', 'Western-Style']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Role-Playing', 'Action RPG', 'Action RPG']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['Role-Playing', 'Action RPG', 'Action RPG']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Action Adventure', 'Modern', 'General', 'Modern', 'Linear']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Action Adventure', 'Horror', 'Horror', 'Survival']
