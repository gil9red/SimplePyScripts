#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from common import seconds_to_str, time_to_seconds


# TODO: возможно, если роликов будет слишком много, не все вернутся из запроса
def parse_playlist_time(url: str) -> (int, List[Tuple[str, str]]):
    """Функция парсит страницу плейлиста и подсчитывает сумму продолжительности роликов."""

    # Передаю невалидный User-Agent чтобы ютуб вернул отрендеренную страницу (данные в HTML будут)
    # а не страницу с скриптом -- данные будут как объект javacript
    headers = {
        'User-Agent': 'null',
    }

    rs = requests.get(url, headers=headers)
    root = BeautifulSoup(rs.content, 'html.parser')

    total_seconds = 0
    items = []

    for tr in root.select('.pl-video-list .pl-video'):
        title = tr['data-title']
        time_str = tr.select_one('.timestamp').text.strip()
        items.append((title, time_str))

        total_seconds += time_to_seconds(time_str)

    return total_seconds, items


if __name__ == '__main__':
    url = 'https://www.youtube.com/playlist?list=PLndO6DOY2cLyxQYX7pkDspTJ42JWx07AO'

    total_seconds, items = parse_playlist_time(url)

    print('Playlist:')

    for i, (title, time) in enumerate(items, 1):
        print('  {}. {} ({})'.format(i, title, time))

    print()
    print('Total time: {} ({} total seconds)'.format(seconds_to_str(total_seconds), total_seconds))
