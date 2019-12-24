#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


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

    url = f'https://iwantgames.ru/?s={game_name}'
    rs = requests.get(url, headers=headers)
    if not rs.ok:
        need_logs and log.warning(f'Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    for game_block in root.select('.game__content'):
        title = get_norm_text(game_block.h2.a)
        if not smart_comparing_names(title, game_name):
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

        genres = [get_norm_text(a) for a in dd.find_all('a')]

        # Сойдет первый, совпадающий по имени, вариант
        genres = get_uniques(genres)

        need_logs and log.info(f'Genres: {genres}')
        return genres

    need_logs and log.info(f'Not found game {game_name!r}')
    return []


if __name__ == '__main__':
    from common import _common_test, TEST_GAMES
    TEST_GAMES.append('Dark Souls: Remastered')

    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: []
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: []
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: []
    #
    # Search 'Twin Sector'...
    #     Genres: []
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: []
    #
    # Search 'Dark Souls: Remastered'...
    #     Genres: ['РПГ', 'Ужасы', 'Экшен']
