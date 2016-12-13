#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    url = 'http://kinokong.net/29053-vse-o-muzhchinah-2016-smotret-online.html'
    import requests
    rs = requests.get(url)

    import re
    match = re.search(r'new.+?Uppod\(.*?file:.*?"(.+?mp4)"', rs.text)
    if match:
        print(match.group(1))
