#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


def search(text: str) -> list[tuple[str, str]]:
    rs = requests.post('https://shop.buka.ru/search', params=dict(q=text))
    rs.raise_for_status()

    items = []
    root = BeautifulSoup(rs.content, 'html.parser')
    for game in root.select('.product-thumb'):
        name = game['data-name']
        price = game['data-price']

        items.append((name, price))

    return items


if __name__ == '__main__':
    text = 'titan'
    for name, price in search(text):
        print(name, price)
