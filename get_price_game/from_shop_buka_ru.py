#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


text = 'titan'

post_data = {
    'search': text,
}

import requests
rs = requests.post('http://shop.buka.ru/search', data=post_data)

from bs4 import BeautifulSoup
root = BeautifulSoup(rs.content, 'lxml')

for game in root.select('.product'):
    name = game.select_one('.name').text.strip()
    price = game.select_one('.costs .c2').text.strip()

    print(name, price)
