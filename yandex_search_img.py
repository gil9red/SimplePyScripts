#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


text = 'Котята'
url = 'http://yandex.ru/images/search?text=' + text

import requests
rs = requests.get(url)
print(rs)

from bs4 import BeautifulSoup
root = BeautifulSoup(rs.content, 'lxml')

from urllib.parse import urljoin

for img in root.select('img.serp-item__thumb'):
    url_img = urljoin(url, img['src'])
    print(url_img)
