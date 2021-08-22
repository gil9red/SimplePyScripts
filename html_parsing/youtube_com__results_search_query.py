#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import json
import re

from dataclasses import dataclass
from typing import List, Optional, Dict, Generator, Callable, Any
from urllib.parse import urljoin

# pip install tzlocal
import tzlocal

# pip install dpath
import dpath.util

import requests


@dataclass
class Video:
    title: str
    url: str

    @classmethod
    def get_from(cls, video: Dict, url: str) -> 'Video':
        try:
            title = dpath.util.get(video, 'title/runs/0/text')
        except KeyError:
            title = dpath.util.get(video, 'title/simpleText')

        url_video = dpath.util.get(video, 'navigationEndpoint/commandMetadata/webCommandMetadata/url')
        url_video = urljoin(url, url_video)

        return cls(title=title, url=url_video)


def get_ytcfg_data(html: str) -> dict:
    m = re.search(r'ytcfg.set\((\{.+?\})\);', html)
    if not m:
        raise Exception('Не удалось найти на странице ytcfg.set!')

    return json.loads(m.group(1))


def dict_merge(d1: dict, d2: dict):
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(v, dict):
            dict_merge(d1[k], v)
        else:
            d1[k] = v


def get_data_for_next_page(url: str, ytcfg_data: dict, continuation_item: dict) -> dict:
    innertube_context = ytcfg_data.get('INNERTUBE_CONTEXT')
    if not innertube_context:
        raise Exception('Значение INNERTUBE_CONTEXT должно быть задано в ytcfg_data!')

    local_zone = tzlocal.get_localzone()
    utc_offset_minutes = local_zone.utcoffset(DT.datetime.now()).total_seconds() // 60

    click_tracking_params = continuation_item['continuationEndpoint']['clickTrackingParams']
    continuation_token = continuation_item['continuationEndpoint']['continuationCommand']['token']

    pattern_next_page_data = {
        "context": {
            "client": {
                "hl": "ru",
                "gl": "RU",
                "remoteHost": "",
                "deviceMake": "",
                "deviceModel": "",
                "visitorData": "",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0,gzip(gfe)",
                "clientName": "WEB",
                "clientVersion": "2.20210816.01.00",
                "osName": "Windows",
                "osVersion": "10.0",
                "originalUrl": url,
                "platform": "DESKTOP",
                "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                "timeZone": str(local_zone),
                "browserName": "Firefox",
                "browserVersion": "91.0",
                "screenWidthPoints": 1280,
                "screenHeightPoints": 548,
                "screenPixelDensity": 1,
                "screenDensityFloat": 1,
                "utcOffsetMinutes": utc_offset_minutes,
                "mainAppWebInfo": {
                    "graftUrl": url,
                    "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                    "isWebNativeShareAvailable": False
                }
            },
            "user": {
                "lockedSafetyMode": False
            },
            "request": {
                "useSsl": True,
                "internalExperimentFlags": [],
                "consistencyTokenJars": []
            },
            "clickTracking": {
                "clickTrackingParams": click_tracking_params
            },
            "adSignalsInfo": {
                "params": [{
                    "key": "dt",
                    "value": ""
                }, {
                    "key": "flash",
                    "value": "0"
                }, {
                    "key": "frm",
                    "value": "0"
                }, {
                    "key": "u_tz",
                    "value": "300"
                }, {
                    "key": "u_his",
                    "value": "1"
                }, {
                    "key": "u_java",
                    "value": "false"
                }, {
                    "key": "u_h",
                    "value": "1024"
                }, {
                    "key": "u_w",
                    "value": "1280"
                }, {
                    "key": "u_ah",
                    "value": "984"
                }, {
                    "key": "u_aw",
                    "value": "1280"
                }, {
                    "key": "u_cd",
                    "value": "24"
                }, {
                    "key": "u_nplug",
                    "value": "0"
                }, {
                    "key": "u_nmime",
                    "value": "0"
                }, {
                    "key": "bc",
                    "value": "31"
                }, {
                    "key": "bih",
                    "value": "548"
                }, {
                    "key": "biw",
                    "value": "1263"
                }, {
                    "key": "brdim",
                    "value": "-1288,40,-1288,40,1280,48,1296,1000,1280,548"
                }, {
                    "key": "vis",
                    "value": "1"
                }, {
                    "key": "wgl",
                    "value": "true"
                }, {
                    "key": "ca_type",
                    "value": "image"
                }
                ]
            }
        },
        "continuation": continuation_token
    }

    dict_merge(pattern_next_page_data['context'], innertube_context)

    return pattern_next_page_data


def get_ytInitialData(html: str) -> Optional[dict]:
    patterns = [
        re.compile(r'window\["ytInitialData"\] = (\{.+?\});'),
        re.compile(r'var ytInitialData = (\{.+?\});'),
    ]

    for pattern in patterns:
        m = pattern.search(html)
        if m:
            data_str = m.group(1)
            return json.loads(data_str)


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'

session = requests.Session()
session.headers['User-Agent'] = USER_AGENT


def get_raw_video_renderer_items(data: Dict) -> List[Dict]:
    for render in ['**/gridVideoRenderer', '**/videoRenderer', '**/playlistVideoRenderer']:
        items = dpath.util.values(data, render)
        if items:
            return items

    return []


def get_generator_raw_video_list(url: str) -> Generator[Dict, None, None]:
    rs = session.get(url)

    data = get_ytInitialData(rs.text)
    if not data:
        raise Exception('Не удалось найти ytInitialData!')

    ytcfg_data = get_ytcfg_data(rs.text)
    innertube_api_key = ytcfg_data['INNERTUBE_API_KEY']

    # Первая порция видео будет в самой странице
    yield from get_raw_video_renderer_items(data)

    # Подгрузка следующих видео
    while True:
        try:
            continuation_item = dpath.util.get(data, '**/continuationItemRenderer')
        except KeyError:
            break

        url_next_page_data = urljoin(rs.url, dpath.util.get(continuation_item, '**/webCommandMetadata/apiUrl'))
        url_next_page_data += '?key=' + innertube_api_key

        next_page_data = get_data_for_next_page(rs.url, ytcfg_data, continuation_item)
        rs = session.post(url_next_page_data, json=next_page_data)
        data = rs.json()

        yield from get_raw_video_renderer_items(data)


def get_raw_video_list(url: str, maximum_items=1000) -> List[Dict]:
    items = []
    for i, video in enumerate(get_generator_raw_video_list(url)):
        if i >= maximum_items:
            break

        items.append(video)

    return items


def get_video_list(url: str, *args, **kwargs) -> List[Video]:
    return [
        Video.get_from(video, url)
        for video in get_raw_video_list(url, *args, **kwargs)
    ]


def search_youtube(text_or_url: str, *args, **kwargs) -> List[Video]:
    if text_or_url.startswith('http'):
        url = text_or_url
    else:
        text = text_or_url
        url = f'https://www.youtube.com/results?search_query={text}'

    return get_video_list(url, *args, **kwargs)


def search_youtube_with_filter(url: str, sort=False, filter_func: Callable[[Any], bool] = None) -> List[str]:
    video_title_list = [video.title for video in search_youtube(url)]
    if sort:
        video_title_list.sort()

    if callable(filter_func):
        video_title_list = list(filter(filter_func, video_title_list))

    return video_title_list


if __name__ == '__main__':
    def __print_video_list(items: List[Video]):
        print(f'Items ({len(items)}):')
        for i, video in enumerate(items, 1):
            print(f'  {i:3}. {video.title!r}: {video.url}')

    url_playlist = 'https://www.youtube.com/playlist?list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r'
    items = get_video_list(url_playlist)
    __print_video_list(items)
    """
    Items (226):
        1. 'Run freeCodeCamp Locally  (P8D2) - Live Coding with Jesse': https://www.youtube.com/watch?v=GFQ9VZYw2-0&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=1
        2. 'React Native Browser Editor  (P8D1) - Live Coding with Jesse': https://www.youtube.com/watch?v=drN9DEm3hFE&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=2
        3. 'React Native Web Styling Part 2  (P7D13) - Live Coding with Jesse': https://www.youtube.com/watch?v=VSLMJ2mZx5Y&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=3
        ...
      224. 'Material Design Cards - Live Coding with Jesse': https://www.youtube.com/watch?v=29ddZX4wjoE&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=224
      225. 'Building a Website: Team Page - Live Coding with Jesse': https://www.youtube.com/watch?v=pfgqJU1lG78&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=225
      226. 'Building a Website (P1D2) - Live Coding with Jesse': https://www.youtube.com/watch?v=rgYQ7nUulAQ&list=PLWKjhJtqVAbknyJ7hSrf1WKh_Xnv9RL1r&index=226
    """

    print('\n' + '-' * 100 + '\n')

    url_playlist = 'https://www.youtube.com/playlist?list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG'
    items = search_youtube(url_playlist)
    __print_video_list(items)
    """
    Items (7):
        1. 'Intro to Java Programming - Course for Absolute Beginners': https://www.youtube.com/watch?v=GoXwIVyNvX0&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=1
        2. 'Functional Programming in Java - Full Course': https://www.youtube.com/watch?v=rPSL1alFIjI&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=2
        3. 'Spring Boot Tutorial for Beginners (Java Framework)': https://www.youtube.com/watch?v=vtPkZShrvXQ&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=3
        4. 'Learn Java 8 - Full Tutorial for Beginners': https://www.youtube.com/watch?v=grEKMHGYyns&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=4
        5. 'Data Structures Easy to Advanced Course - Full Tutorial from a Google Engineer': https://www.youtube.com/watch?v=RBSGKlAvoiM&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=5
        6. 'Spring Boot and Angular Tutorial - Build a Reddit Clone (Coding Project)': https://www.youtube.com/watch?v=DKlTBBuc32c&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=6
        7. 'Android Development for Beginners - Full Course': https://www.youtube.com/watch?v=fis26HvvDII&list=PLWKjhJtqVAbnRT_hue-3zyiuIYj0OlpyG&index=7
    """

    print('\n' + '-' * 100 + '\n')

    # Testing for: youtube, channel, channel videos
    print(len(get_video_list('https://www.youtube.com/')))
    print(len(get_video_list('https://www.youtube.com/c/TheBadComedian')))
    print(len(get_video_list('https://www.youtube.com/c/TheBadComedian/videos')))
    # 247
    # 45
    # 190

    print('\n' + '-' * 100 + '\n')

    items = search_youtube('щенки', maximum_items=25)
    __print_video_list(items)
    """
    Items (25):
        1. '🐾 Дружные мопсы - Серия 1 Сезон 1 - Мультфильмы Disney': https://www.youtube.com/watch?v=Eqyz-bFtkEM
        2. 'Лучшие Приколы про собак | Подборка приколов про собак и щенков #8': https://www.youtube.com/watch?v=wNqZM7e0_18
        3. 'СМЕШНЫЕ СОБАКИ И ЩЕНКИ 2020': https://www.youtube.com/watch?v=Grjk1K0YPSU
        ...
       23. 'Щенячий патруль и Мегащенки  Новые серии - 2021': https://www.youtube.com/watch?v=Gq63Zl0OL4k
       24. 'КАК ЩЕНКИ РАДУЮТСЯ МОЕМУ ПРИХОДУ АЛАБАЙ / КАК ЩЕНКИ АЛАБАЙ ЗАБАВНО БАЛУЮТСЯ': https://www.youtube.com/watch?v=QaMebbbCQ9E
       25. 'Макс и Катя играют с сюрпризами в огромных яйцах': https://www.youtube.com/watch?v=Mt7oS8Yq8YY
    """

    print('\n' + '-' * 100 + '\n')

    items = search_youtube('https://www.youtube.com/results?search_query=slipknot official', maximum_items=50)
    __print_video_list(items)
    """
    Items (50):
        1. 'Knotfest Los Angeles 2021: On-Sale Now': https://www.youtube.com/watch?v=8ueHLoI8htY
        2. 'Joey Jordison: 1975 - 2021': https://www.youtube.com/watch?v=5hejcY2p4A4
        3. 'Knotfest Los Angeles: November 5, 2021 [TRAILER]': https://www.youtube.com/watch?v=9qXnhQ0p7FA
        ...
       48. 'Slipknot: Live at Download Festival 2019': https://www.youtube.com/watch?v=QO3j9niG1Og
       49. 'Slipknot - Orphan (Audio)': https://www.youtube.com/watch?v=dvLp3XPNAZ0
       50. 'Slipknot - Spit It Out [OFFICIAL VIDEO]': https://www.youtube.com/watch?v=ZPUZwriSX4M
    """

    print('\n' + '-' * 100 + '\n')

    url = 'https://www.youtube.com/playlist?list=PLZfhqd1-Hl3DtfKRjleAWB-zYJ-pj7apK'
    items = search_youtube_with_filter(url)
    print(f'Items ({len(items)}): {items}')
    # Items (3): ['История серии Diablo. Акт I', 'История серии Diablo. Акт II', 'История серии Diablo. Акт III']

    print('\n' + '-' * 100 + '\n')

    text = 'Gorgeous Freeman -'
    url = 'https://www.youtube.com/user/antoine35DeLak/search?query=' + text
    items = search_youtube_with_filter(url)
    print(f'Items ({len(items)}): {items}')
    # Items (46): ['Gorgeous Freeman - Episode 1 - The Suit', ..., 'The Epileptic Seizure [Gmod]']

    items = search_youtube_with_filter(url, filter_func=lambda name: text in name)
    print(f'Filtered items ({len(items)}): {items}')
    # Filtered items (3): ['Gorgeous Freeman - Episode 1 - The Suit', 'Gorgeous Freeman - Episode 3 - The Part 1', 'Gorgeous Freeman - Episode 2 - The Crowbar']

    print('\n' + '-' * 100 + '\n')

    text = 'Sally Face'
    url = 'https://www.youtube.com/user/HellYeahPlay/search?query=' + text
    items = search_youtube_with_filter(url)
    print(f'Items ({len(items)}): {items}')
    # Items (244): ['ТВОРЕНИЯ ВЕЛЬЗЕВУЛА - Sally Face [ЭПИЗОД 4] #9', ..., 'ЛЕСБИЙСКИЙ ТРЭШНЯК - Love Is Strange']

    items = search_youtube_with_filter(url, filter_func=lambda name: text in name and 'эпизод' in name.lower())
    print(f'Filtered items ({len(items)}): {items}')
    # Filtered items (14): ['ТВОРЕНИЯ ВЕЛЬЗЕВУЛА - Sally Face [ЭПИЗОД 4] #9', ..., 'ПОИСК МЕРТВЫХ ЛЮДЕЙ ☠️ Sally Face [ЭПИЗОД 2] #4']
