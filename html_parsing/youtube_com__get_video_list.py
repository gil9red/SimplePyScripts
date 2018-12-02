#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Callable, Any


def get_video_list(url: str, sort=False, filter_func: Callable[[Any], bool]=None) -> List[str]:
    import requests
    rs = requests.get(url)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'html.parser')

    video_title_list = [x.text.strip() for x in root.select('.yt-lockup-title > a')]

    if sort:
        video_title_list.sort()

    if callable(filter_func):
        video_title_list = list(filter(filter_func, video_title_list))

    return video_title_list


if __name__ == '__main__':
    text = 'Gorgeous Freeman -'
    url = 'https://www.youtube.com/user/antoine35DeLak/search?query=' + text
    items = get_video_list(url)
    print('Items ({}): {}'.format(len(items), items))

    items = get_video_list(url, filter_func=lambda name: text in name)
    print('Items ({}): {}'.format(len(items), items))

    print()

    text = 'Sally Face'
    url = 'https://www.youtube.com/user/HellYeahPlay/search?query=' + text
    items = get_video_list(url)
    print('Items ({}): {}'.format(len(items), items))

    items = get_video_list(url, filter_func=lambda name: text in name and 'эпизод' in name.lower())
    print('Items ({}): {}'.format(len(items), items))
