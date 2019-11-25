#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple

import requests

from common import smart_comparing_names


def search_game_genres(game_name: str) -> List[Tuple[str, List[str]]]:
    headers = {
        'Host': 'ag.ru',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
    }

    session = requests.session()
    rs = session.get('https://ag.ru/games/pc', headers=headers)
    if not rs.ok:
        print(f'[-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
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
        print(f'[-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    items = []

    for item in rs.json()['results']:
        # Если игра была на PC
        if not any(x['platform']['name'] == 'PC' for x in item.get('platforms', [])):
            continue

        genres = [x['name'] for x in item['genres']]
        if not genres:
            continue

        title = item['name']
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
    #   Result (3):
    #     'Hellgate: London': ['Шутеры', 'Экшены', 'Ролевые']
    #     'One day in London': ['Казуальные', 'Инди', 'Приключения']
    #     "London's Burning!": ['Шутеры']
    #
    # Genres: ['Шутеры', 'Экшены', 'Ролевые']
    #
    # --------------------
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #   Result (4):
    #     'Van Helsing. Новая история': ['Инди', 'Экшены', 'Ролевые']
    #     'The Incredible Adventures of Van Helsing: Final Cut': ['Инди', 'Приключения', 'Экшены', 'Ролевые']
    #     'Van Helsing 2: Смерти вопреки': ['Инди', 'Приключения', 'Экшены', 'Ролевые']
    #     'The Incredible Adventures of Van Helsing III': ['Инди', 'Приключения', 'Экшены', 'Ролевые']
    #
    # Genres: []
    #
    # --------------------
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #   Result (5):
    #     'Dark Souls: Prepare To Die Edition': ['Экшены', 'Ролевые']
    #     'Kart Souls: Prepare To Ride Edition': ['Ролевые']
    #     'Dark Souls: Remastered': ['Экшены']
    #     'Teleglitch: Die More Edition': ['Инди', 'Экшены']
    #     'Обитель тьмы: Сумерки': ['Инди', 'Приключения']
    #
    # Genres: ['Экшены', 'Ролевые']
    #
    # --------------------
    #
    # Search 'Twin Sector'...
    #   Result (4):
    #     'Twin Sector': ['Приключения', 'Экшены']
    #     'Twin Win v1.0': ['Платформеры']
    #     'SECTOR': ['Инди', 'Экшены']
    #     'Hector: Episode 2': ['Казуальные', 'Приключения']
    #
    # Genres: ['Приключения', 'Экшены']
    #
    # --------------------
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #   Result (5):
    #     'Call of Cthulhu: Dark Corners of the Earth': ['Шутеры']
    #     'Call of Cthulhu: Shadow of the Comet': ['Приключения']
    #     'Call of Cthulhu: Prisoner of Ice': ['Приключения']
    #     'Call of Cthulhu: The Wasted Land': ['Приключения', 'Экшены', 'Ролевые', 'Стратегии', 'Инди']
    #     'Odallus: The Dark Call': ['Инди', 'Приключения', 'Экшены']
    #
    # Genres: ['Шутеры']
    #
    # --------------------
