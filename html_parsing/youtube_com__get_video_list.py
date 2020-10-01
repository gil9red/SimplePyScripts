#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Callable, Any

from youtube_com__results_search_query import search_youtube


def get_video_list(url: str, sort=False, filter_func: Callable[[Any], bool] = None) -> List[str]:
    video_title_list = [title for url, title in search_youtube(url)]
    if sort:
        video_title_list.sort()

    if callable(filter_func):
        video_title_list = list(filter(filter_func, video_title_list))

    return video_title_list


if __name__ == '__main__':
    text = 'Gorgeous Freeman -'
    url = 'https://www.youtube.com/user/antoine35DeLak/search?query=' + text
    items = get_video_list(url)
    print(f'Items ({len(items)}): {items}')

    items = get_video_list(url, filter_func=lambda name: text in name)
    print(f'Filtered items ({len(items)}): {items}')

    print()

    text = 'Sally Face'
    url = 'https://www.youtube.com/user/HellYeahPlay/search?query=' + text
    items = get_video_list(url)
    print(f'Items ({len(items)}): {items}')

    items = get_video_list(url, filter_func=lambda name: text in name and 'эпизод' in name.lower())
    print(f'Filtered items ({len(items)}): {items}')
