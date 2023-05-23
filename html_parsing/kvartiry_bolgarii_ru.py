#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


rs = requests.get(
    "https://kvartiry-bolgarii.ru/neveroyatnaya-kvartira-s-vidom-na-more-tip-pentkhaus-o26253"
)
root = BeautifulSoup(rs.content, "html.parser")

urls = [
    urljoin(rs.url, img["src"])
    for img in root.select("#slider > li > img[src]")
]
print(urls)
# ['https://kvartiry-bolgarii.ru/photos/5e2c79b4-7da2-478e-a783-ad8f010d0b15.jpg', ... afc9-ad8f010e2703.jpg']

coords = root.select_one("#map[data-coords]")
print(coords["data-coords"])
# 42.6399264:27.6781406

latitude, longitude = coords["data-coords"].split(":")
print(latitude, longitude)
# 42.6399264 27.6781406
