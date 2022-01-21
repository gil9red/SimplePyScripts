#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
import requests


session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'


URL_BRAND = 'https://goldapple.ru/brands/elian-russia'


rs = session.get(URL_BRAND)
m = re.search(r'"productsApiUrl":\s*"(.+?)",', rs.text)
if not m:
    raise Exception('Не получилось найти ссылку на API!')

URL_API_PRODUCTS = m.group(1)

print(f'Using API: {URL_API_PRODUCTS}')
# Using API: https://goldapple.ru/web_scripts/discover/category/products?cat=6577


total = 0
page = 1
while True:
    rs = session.get(URL_API_PRODUCTS, params={'page': page})
    rs.raise_for_status()

    products = rs.json().get('products')
    if not products:
        break

    total += len(products)

    page += 1

print(total)
# 27
