#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


rs = requests.get('https://freelance.habr.com/tasks?q=python')
root = BeautifulSoup(rs.content, 'html.parser')
urls = [
    urljoin(rs.url, a['href'])
    for a in root.select('.task__title > a[href]')
]
print(len(urls), urls)
# 25 ['https://freelance.habr.com/tasks/349681', ..., 'https://freelance.habr.com/tasks/348667']
