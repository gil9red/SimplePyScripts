#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple

import requests
from bs4 import BeautifulSoup


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/f0403620f7948306ad9e34a373f2aabc0237fb2a/seconds_to_str.py
def seconds_to_str(seconds: int) -> str:
    hh, mm = divmod(seconds, 3600)
    mm, ss = divmod(mm, 60)
    return "%02d:%02d:%02d" % (hh, mm, ss)


def time_to_seconds(time_str: str) -> int:
    time_split = list(map(int, time_str.split(':')))

    if len(time_split) == 3:
        h, m, s = time_split
        return h * 60 * 60 + m * 60 + s

    elif len(time_split) == 2:
        m, s = time_split
        return m * 60 + s

    else:
        return time_split[0]


# TODO: возможно, если роликов будет слишком много, не все вернутся из запроса
def parse_playlist_time(url) -> (int, List[Tuple[str, str]]):
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
