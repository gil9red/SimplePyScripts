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
        'mode': '11',
        's': '1',
        'p': '1',
        'fg': 'all',
        'fp': 'pc',
        'fn': game_name
    }

    url = 'https://www.igromania.ru/-Engine-/AJAX/games.list.v2/index.php'
    rs = requests.post(url, headers=headers, data=form_data)
    if not rs.ok:
        need_logs and print(f'[-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    for game_block in root.select('.gamebase_box'):
        title = get_norm_text(game_block.select_one('.release_name'))
        if not smart_comparing_names(title, game_name):
            continue

        genres = [get_norm_text(a) for a in game_block.select('.genre > a')]

        # Сойдет первый, совпадающий по имени, вариант
        return genres

    return []


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # TODO: добавить пример вывода
