#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import requests


GET_VIDEO_URL_PATTERN = re.compile("video_url=(.+?)&amp")


def get_video_url(url):
    rs = requests.get(url)
    if not rs.ok:
        return

    match = GET_VIDEO_URL_PATTERN.search(rs.text)
    if match:
        return match.group(1)


if __name__ == "__main__":
    url = "http://www.trahun.org/video-zadnica-molodoy-suchki.html"
    print(get_video_url(url))

    url = "http://www.trahun.org/video-goryachaya-mamochka-s-silikonovymi-siskami.html"
    print(get_video_url(url))

    url = "http://www.trahun.org/video-beluyu-devushku-jestko-trahayut-zdorovye-negry.html"
    print(get_video_url(url))
