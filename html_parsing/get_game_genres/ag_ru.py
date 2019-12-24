#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

import requests

from common import smart_comparing_names, USER_AGENT, get_uniques, get_logger


log = get_logger(__file__)


def get_game_genres(game_name: str, need_logs=False) -> List[str]:
    need_logs and log.info(f'Search {game_name!r}...')

    headers = {
        'Host': 'ag.ru',
        'User-Agent': USER_AGENT,
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
    }

    session = requests.session()
    rs = session.get('https://ag.ru/games/pc', headers=headers)
    if not rs.ok:
        need_logs and log.warning(f'Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    # Заголовки, что отправляются вместе с запросом к API
    headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Referer': 'https://ag.ru/games/pc',
        'X-API-Language': 'ru',
        'X-API-Referer': '%2Fgames',
        'X-API-Client': 'website',
    })

    # По умолчанию, page_size=20, но столько результатов не нужно. По хорошему, можно page_size=1, но есть
    # шанс, что игра, что ищем сервером вернется не в первых позициях
    rs = session.get(f'https://ag.ru/api/games?page_size=5&search={game_name}&page=1', headers=headers)
    if not rs.ok:
        need_logs and log.warning(f'Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    for item in rs.json()['results']:
        title = item['name']
        if not smart_comparing_names(title, game_name):
            continue

        genres = [x['name'] for x in item['genres']]

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
    #     Genres: ['Шутеры', 'Экшены', 'Ролевые']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: []
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: ['Экшены', 'Ролевые']
    #
    # Search 'Twin Sector'...
    #     Genres: ['Приключения', 'Экшены']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Шутеры']
