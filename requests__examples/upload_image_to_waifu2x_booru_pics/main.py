#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import requests


URL = "https://waifu2x.booru.pics/Home/upload"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65",
}
DATA = {
    "denoise": "1",
    "scale": "1",
}
FILES = {"img": open("image.jpg", "rb")}

with requests.session() as s:
    s.headers.update(HEADERS)

    rs = s.post(URL, files=FILES, data=DATA)
    print(rs.url)
    # https://waifu2x.booru.pics/Home/status?handle=H%3Awaifu2x.slayerduck.com%3A2949305&hash=c8a984fc10b416869ca04c8f8629d429d4b28461_s1_n1

    # Ждем пока файл обработается на сервере
    while "/Home/status?" in rs.url:
        rs = s.get(rs.url)
        time.sleep(0.5)

    print(rs.url)
    # https://waifu2x.booru.pics/Home/show?hash=c8a984fc10b416869ca04c8f8629d429d4b28461_s1_n1
