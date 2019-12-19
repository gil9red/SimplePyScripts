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
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://gamebomb.ru',
        'Referer': 'http://gamebomb.ru/games',
        'Accept': 'application/json',
    }
    data = {
        'query': game_name,
        'type': '',
    }

    session = requests.session()
    session.headers.update(headers)

    url = f'http://gamebomb.ru/base/ajaxSearch'
    rs = session.post(url, data=data)
    if not rs.ok:
        need_logs and print(f'  [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    for game_block_preview in rs.json():
        if game_block_preview['type'] != 'игра':
            continue

        title = game_block_preview['title']
        if not smart_comparing_names(title, game_name):
            continue

        url_game = urljoin(rs.url, game_block_preview['url'])
        need_logs and print(f'  [+] Load {url_game!r}')

        rs = session.get(url_game)
        if not rs.ok:
            need_logs and print(f'    [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
            continue

        game_block = BeautifulSoup(rs.content, 'html.parser')
        # <tr>
        #     <td valign="top">Жанры</td>
        #     <td>
        #         <div>
        #             <input type="hidden" class="edit hidden" name="genres[18]" value="0">
        #             <input type="checkbox" checked="checked" class="edit hidden" name="genres[18]" value="1">
        #             Шутер от первого лица
        #         </div>
        #         <div>
        #             <input type="hidden" class="edit hidden" name="genres[2]" value="0">
        #             <input type="checkbox" checked="checked" class="edit hidden" name="genres[2]" value="1">
        #             Боевик-приключения
        #         </div>
        game_block = game_block.find('td', text='Жанры')
        if not game_block:
            continue

        genres = []
        for div in game_block.find_next_sibling('td').find_all('div'):
            if not div.select('input[name*="genres"]'):
                continue

            genres.append(get_norm_text(div))

        # Сойдет первый, совпадающий по имени, вариант
        return genres

    return []


if __name__ == '__main__':
    from common import _common_test
    _common_test(get_game_genres)

    # Search 'Hellgate: London'...
    #     Genres: ['Боевик/Экшн', 'Ролевые игры', 'Шутер от первого лица', 'ММОРПГ/Многопользоватеские онлайновые']
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    #     Genres: ['Боевик/Экшн', 'Ролевые игры']
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    #     Genres: []
    #
    # Search 'Twin Sector'...
    #     Genres: ['Головоломки/Пазл', 'Шутер от первого лица']
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    #     Genres: ['Боевик/Экшн', 'Приключения', 'Шутер от первого лица']
