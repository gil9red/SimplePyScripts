#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple

import re
import json
import requests

from common import seconds_to_str


def get_video_list(data: dict) -> list:
    video_list = data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']
    return [video['playlistVideoRenderer'] for video in video_list]


def get_ytInitialData(text: str) -> dict:
    m = re.search('window\["ytInitialData"\] = ({.+?});', text)
    if not m:
        raise Exception("""Не получилось найти 'window["ytInitialData"] = {...'""")

    text = m.group(1)
    return json.loads(text)


# TODO: возможно, если роликов будет слишком много, не все вернутся из запроса
def parse_playlist_time(url: str) -> (int, List[Tuple[str, str]]):
    """Функция парсит страницу плейлиста и подсчитывает сумму продолжительности роликов."""

    # Передаю User-Agent чтобы ютуб вернул страницу с скриптом -- данные будут как объект javacript
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    }

    rs = requests.get(url, headers=headers)
    data = get_ytInitialData(rs.text)

    total_seconds = 0
    items = []

    for video in get_video_list(data):
        title = video['title']['simpleText']
        duration_text = video['lengthText']['simpleText']
        duration_secs = int(video['lengthSeconds'])

        total_seconds += duration_secs
        items.append((title, duration_text))

    return total_seconds, items


if __name__ == '__main__':
    url = 'https://www.youtube.com/playlist?list=PLndO6DOY2cLyxQYX7pkDspTJ42JWx07AO'

    total_seconds, items = parse_playlist_time(url)

    print('Playlist:')

    for i, (title, time) in enumerate(items, 1):
        print('  {}. {} ({})'.format(i, title, time))

    print()
    print('Total time: {} ({} total seconds)'.format(seconds_to_str(total_seconds), total_seconds))
