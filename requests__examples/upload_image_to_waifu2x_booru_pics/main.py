#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests

URL = "https://waifu2x.booru.pics/Home/upload"
HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65",
}
DATA = {
    'denoise': '1',
    'scale': '2',
}
FILES = {
    'img': open('image.jpg', 'rb')
}

rs = requests.post(URL, headers=HEADERS, files=FILES, data=DATA)

# NOTE: need check status and redirect
print(rs.url)
# https://waifu2x.booru.pics/Home/status?handle=H%3Awaifu2x.slayerduck.com%3A2949160&hash=f3430bb9886bb97472bc6111e9c568bba9915e4a_s2_n1
