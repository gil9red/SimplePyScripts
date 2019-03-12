#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


text = 'Gorgeous Freeman - '

import requests
rs = requests.get('https://www.youtube.com/user/antoine35DeLak/search?query=' + text)

from bs4 import BeautifulSoup
root = BeautifulSoup(rs.content, 'lxml')

# Get video list and filter by <text>
gorgeous_video_list = list(filter(lambda x: x.startswith(text), (x.text for x in root.select('.yt-lockup-title > a'))))
print(len(gorgeous_video_list), sorted(gorgeous_video_list))
