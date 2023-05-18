#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import requests


def get_video_url(url):
    rs = requests.get(url)

    match = re.search(r'new.+?Uppod\(.*?file:.*?"(.+?mp4)"', rs.text)
    if match:
        return match.group(1)


if __name__ == "__main__":
    url = "http://kinokong.net/29053-vse-o-muzhchinah-2016-smotret-online.html"
    print(get_video_url(url))
