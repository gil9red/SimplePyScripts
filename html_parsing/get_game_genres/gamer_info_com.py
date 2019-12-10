#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

from bs4 import BeautifulSoup
import requests

from common import smart_comparing_names, USER_AGENT, get_norm_text


def get_game_genres(game_name: str, need_logs=False) -> List[str]:
    headers = {
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',
    }
    form_data = {
        'search-query': game_name,
        'search-obl': 'games',
        'page': '1',
    }

    rs = requests.post('https://gamer-info.com/search-q/', headers=headers, data=form_data)
    if not rs.ok:
        need_logs and print(f'[-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    for game_block in root.select('.games > .c2'):
        g = game_block.select_one('.g')
        if 'Жанр:' not in g.text:
            continue

        title = get_norm_text(game_block.select_one('.n'))
        if not smart_comparing_names(title, game_name):
            continue

        genres = g.text.replace('Жанр:', '').strip().split(', ')

        # Сойдет первый, совпадающий по имени, вариант
        return genres

    return []


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # TODO: добавить пример вывода
