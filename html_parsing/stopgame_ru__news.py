#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_news(url: str) -> list:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    items = []
    for item in root.select('.item.article-summary'):
        title = item.select_one('.caption').get_text(strip=True)
        url_news = urljoin(rs.url, item.select_one('.caption > a')['href'])
        date_str = item.select_one('.info-item.timestamp').get_text(strip=True)

        items.append((title, url_news, date_str))

    return items


if __name__ == '__main__':
    items = get_news('https://stopgame.ru/news')
    for x in items:
        print(x)
