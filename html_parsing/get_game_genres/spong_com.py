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
    }

    url = f'https://spong.com/search/index.jsp?q={game_name}'
    rs = requests.get(url, headers=headers)
    if not rs.ok:
        need_logs and print(f'[-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    # Первая таблица -- та, что нужна нам
    for game_block in root.select_one('table.searchResult').select('tr'):
        tds = game_block.select('td')

        # Например, tr > th
        if len(tds) != 4:
            continue

        td_title, _, genres_td, platforms_td = tds

        title = get_norm_text(td_title.a)
        if not smart_comparing_names(title, game_name):
            continue

        # Если игра не была на PC
        if not any('PC' in a.text.upper() for a in platforms_td.select('a')):
            continue

        # <td>Adventure: Free Roaming<br/>Adventure: Survival Horror<br/></td>
        #   -> ['Adventure: Free Roaming', 'Adventure: Survival Horror']
        genres = list(genres_td.stripped_strings)

        # Сойдет первый, совпадающий по имени, вариант
        return genres

    return []


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # TODO: добавить пример вывода
