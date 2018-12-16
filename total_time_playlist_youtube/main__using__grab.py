#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple

from common import seconds_to_str, time_to_seconds


PROXY = ''
PROXY_TYPE = ''


# TODO: возможно, если роликов будет слишком много, не все вернутся из запроса
def parse_playlist_time(url: str) -> (int, List[Tuple[str, str]]):
    """Функция парсит страницу плейлиста и подсчитывает сумму продолжительности роликов."""

    import grab
    g = grab.Grab()

    if PROXY:
        g.setup(proxy=PROXY, proxy_type=PROXY_TYPE)

    # Передаю невалидный User-Agent чтобы ютуб вернул отрендеренную страницу (данные в HTML будут)
    # а не страницу с скриптом -- данные будут как объект javacript
    g.setup(headers={'User-Agent': 'null'})

    g.go(url)

    video_list = g.doc.select('//*[@class="pl-video yt-uix-tile "]')
    time_list = g.doc.select('//*[@class="timestamp"]')

    total_seconds = 0
    items = []

    for title, time in zip(video_list, time_list):
        title = title.attr('data-title')
        time_str = time.text()
        items.append((title, time_str))

        total_seconds += time_to_seconds(time_str)

    return total_seconds, items


if __name__ == '__main__':
    # url = 'https://www.youtube.com/playlist?list=PLqf5JRBicHXnV4fUNPJtE2YFAjPMHRX4K'
    # url = 'https://www.youtube.com/playlist?list=PLKom48yw6lJpyYN2Q_zmss68ntjzxxpHd'
    # url = 'https://www.youtube.com/playlist?list=PLvX4-HTvsLu-j-K9n14cV5OvxwBl_8Won'
    url = 'https://www.youtube.com/playlist?list=PLndO6DOY2cLyxQYX7pkDspTJ42JWx07AO'

    total_seconds, items = parse_playlist_time(url)

    print('Playlist:')

    for i, (title, time) in enumerate(items, 1):
        print('  {}. {} ({})'.format(i, title, time))

    print()
    print('Total time: {} ({} total seconds)'.format(seconds_to_str(total_seconds), total_seconds))
