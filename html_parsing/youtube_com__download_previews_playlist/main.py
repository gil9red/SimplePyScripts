#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import re
import sys
from pathlib import Path

# pip install dpath
import dpath.util

import requests

sys.path.append('../..')
from get_valid_filename import get_valid_filename


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
PATTERN = re.compile(r'window\["ytInitialData"\] = (\{.+?\});')

PATTERN_URL_PLAYLIST = 'https://www.youtube.com/playlist?list={playlist_id}'
PATTERN_URL_VIDEO_PREVIEW = 'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg'


session = requests.Session()
session.headers['User-Agent'] = USER_AGENT


def download_playlist_video_previews(playlist_id: str):
    url = PATTERN_URL_PLAYLIST.format(playlist_id=playlist_id)

    rs = session.get(url)
    m = PATTERN.search(rs.text)
    if not m:
        print('Not found "ytInitialData"!')
        return

    data_str = m.group(1)
    data = json.loads(data_str)

    playlist_title = dpath.util.get(data, '**/playlistMetadataRenderer/title')
    safe_playlist_title = get_valid_filename(playlist_title)

    dir_name = Path(f'{safe_playlist_title}. {playlist_id}')
    dir_name.mkdir(parents=True, exist_ok=True)

    videos = dpath.util.values(data, '**/playlistVideoRenderer')

    for video in videos:
        video_id = video['videoId']
        seq = video['index']['simpleText']
        title = video['title']['simpleText']

        safe_title = get_valid_filename(title)
        file_name = dir_name / f'{seq}. {safe_title}. {video_id}.jpg'

        url_img = PATTERN_URL_VIDEO_PREVIEW.format(video_id=video_id)
        img_data = session.get(url_img).content
        file_name.write_bytes(img_data)


if __name__ == '__main__':
    download_playlist_video_previews('PLKom48yw6lJrkPuqimEiH3PT1ibALMh0k')
    download_playlist_video_previews('PLejGw9J2xE9XCDw_lFIo9RJCnzpr6P_0Z')
