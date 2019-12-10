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

    url = f'https://www.mobygames.com/search/quick?q={game_name}&p=3&search=Go&sFilter=1&sG=on'
    rs = session.get(url)
    if not rs.ok:
        need_logs and print(f'  [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    for game_block_preview in root.select('.searchTitle > a'):
        title = get_norm_text(game_block_preview)

        if not smart_comparing_names(title, game_name):
            continue

        href = game_block_preview['href']
        url_game = urljoin(rs.url, href)

        need_logs and print(f'  [+] Load {url_game!r}')

        rs = session.get(url_game)
        if not rs.ok:
            need_logs and print(f'    [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
            return []

        game_block = BeautifulSoup(rs.content, 'html.parser')

        genres = game_block\
            .select_one('#coreGameGenre').find_next('div', text='Genre')\
            .find_next_sibling('div').find_all('a')

        genres = [get_norm_text(a) for a in genres]

        # Сойдет первый, совпадающий по имени, вариант
        return genres

    return []


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Role-Playing (RPG)']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Action', 'Role-Playing (RPG)']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['Action', 'Role-Playing (RPG)']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Action']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Action']
