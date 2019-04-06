#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from bs4 import BeautifulSoup
import requests


rs = requests.get('http://sushivkusno.com/category/nabory-siety')
print(rs)

root = BeautifulSoup(rs.content, 'lxml')
items = root.select('.CardContent')

for i, product in enumerate(items, 1):
    title = product.select_one('.CardText__title').text
    weight = product.select_one('.CardText__subtitle > span > b').text

    price = product.select_one('.ProductParams__price').text
    price = int(re.sub('\D', '', price))

    print('{}. "{}": {}, {}'.format(i, title, weight, price))
