#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
from typing import List, Tuple, Optional
import re

# pip install dpath
import dpath.util

import requests


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
PATTERN = re.compile(r'window\["ytInitialData"\] = (\{.+?\});')


session = requests.Session()
session.headers['User-Agent'] = USER_AGENT


def get_ytInitialData(url: str) -> Optional[dict]:
    rs = session.get(url)
    m = PATTERN.search(rs.text)
    if not m:
        return

    data_str = m.group(1)
    return json.loads(data_str)


def search_youtube(text_or_url: str) -> List[Tuple[str, str]]:
    if text_or_url.startswith('http'):
        url = text_or_url
    else:
        text = text_or_url
        url = f'https://www.youtube.com/results?search_query={text}'

    items = []

    data = get_ytInitialData(url)
    if not data:
        return items

    result = dpath.util.values(data, '**/videoRenderer')
    for video in result:
        if 'videoId' not in video:
            continue

        url = 'https://www.youtube.com/watch?v=' + video['videoId']
        try:
            title = dpath.util.get(video, 'title/runs/0/text')
        except KeyError:
            title = dpath.util.get(video, 'title/simpleText')

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
