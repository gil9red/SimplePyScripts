#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
from typing import List, Tuple
import re

# pip install dpath
import dpath.util

import requests


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
PATTERN = re.compile(r'window\["ytInitialData"\] = (\{.+?\});')


def search_youtube(text: str) -> List[Tuple[str, str]]:
    url = f'https://www.youtube.com/results?search_query={text}'

    items = []

    rs = requests.get(url, headers={'User-Agent': USER_AGENT})
    m = PATTERN.search(rs.text)
    if not m:
        return items

    data_str = m.group(1)
    data = json.loads(data_str)

    result = dpath.util.values(data, '**/videoRenderer')
    for video in result:
        if 'videoId' not in video:
            continue

        url = 'https://www.youtube.com/watch?v=' + video['videoId']
        title = dpath.util.get(video, 'title/runs/0/text')

        items.append((url, title))

    return items


if __name__ == '__main__':
    items = search_youtube('щенки')
    print(f'Items({len(items)}):')
    for i, (url, title) in enumerate(items, 1):
        print(f'    {i:2}. {url} {title!r}')

    print('\n' + '-' * 100 + '\n')

    items = search_youtube('slipknot official')
    print(f'Items({len(items)}):')
    for i, (url, title) in enumerate(items, 1):
        print(f'    {i:2}. {url} {title!r}')

    # Items(38):
    #      1. https://www.youtube.com/watch?v=69LWIejU6ro 'Slipknot - Unsainted (Behind The Scenes)'
    #      2. https://www.youtube.com/watch?v=mv6XO96Om-I 'Slipknot - Pollution'
    #      3. https://www.youtube.com/watch?v=JGNqvH9ykfA 'Slipknot - Nero Forte [OFFICIAL VIDEO]'
    #      4. https://www.youtube.com/watch?v=i9GGg_yadQU 'Slipknot - Europe & UK 2020 Tour Announce'
    #      5. https://www.youtube.com/watch?v=ZHKVeLTt6Xc "Alexa: Play 'We Are Not Your Kind' by Slipknot (Amazon Music)"
    # ...
