#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/f0403620f7948306ad9e34a373f2aabc0237fb2a/seconds_to_str.py
def seconds_to_str(seconds: int) -> str:
    hh, mm = divmod(seconds, 3600)
    mm, ss = divmod(mm, 60)
    return "%02d:%02d:%02d" % (hh, mm, ss)


# TODO: возможно, если роликов будет слишком много, не все вернутся из запроса
def parse_playlist_time(url, proxy=None, proxy_type='http') -> (int, List[Tuple[str, str]]):
    """Функция парсит страницу плейлиста и подсчитывает сумму продолжительности роликов."""

    import grab
    g = grab.Grab()
    if proxy:
        g.setup(proxy=proxy, proxy_type=proxy_type)

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

        time_split = time_str.split(':')
        if len(time_split) == 3:
            h, m, s = map(int, time_split)
            total_seconds += h * 60 * 60 + m * 60 + s
        elif len(time_split) == 2:
            m, s = map(int, time_split)
            total_seconds += m * 60 + s
        else:
            total_seconds += int(time_split[0])

    return total_seconds, items


if __name__ == '__main__':
    url = 'https://www.youtube.com/playlist?list=PLqf5JRBicHXnV4fUNPJtE2YFAjPMHRX4K'
    # url = 'https://www.youtube.com/playlist?list=PLKom48yw6lJpyYN2Q_zmss68ntjzxxpHd'
    url = 'https://www.youtube.com/playlist?list=PLvX4-HTvsLu-j-K9n14cV5OvxwBl_8Won'
    url = 'https://www.youtube.com/playlist?list=PLndO6DOY2cLyxQYX7pkDspTJ42JWx07AO'

    import config
    total_seconds, items = parse_playlist_time(url, config.proxy, config.proxy_type)

    print('Playlist:')

    for i, (title, time) in enumerate(items, 1):
        print('  {}. {} ({})'.format(i, title, time))

    print()
    print('Total time: {} ({} total seconds)'.format(seconds_to_str(total_seconds), total_seconds))
