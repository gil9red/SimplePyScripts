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

    url = f'https://www.gamespot.com/search/?i=site&q={game_name}'
    rs = session.get(url)
    if not rs.ok:
        need_logs and log.warning(f'Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    for game_block_preview in root.select('.media-body'):
        if not game_block_preview.select_one('.media-date'):
            continue

        a = game_block_preview.select_one('.media-title a')
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
        tag_object_stats = game_block.select_one('#object-stats-wrap')
        if not tag_object_stats:
            return []

        genres = [get_norm_text(a) for a in tag_object_stats.select('a[href]') if '/genre/' in a['href']]

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
    #     Genres: ['Role-Playing']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Role-Playing', 'Action']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: []
    #
    # Search 'Twin Sector'...
    #     Genres: ['Action', 'Adventure']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Adventure', 'Survival', '3D', 'Action']
