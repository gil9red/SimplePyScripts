#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
session = requests.session()
rs = session.get('http://gepur.ru/product/plate-6917')
html = rs.text

# Ищем следующую строку c описанием модели
re_expr = r'ProductPage\.init\((.+)\)'

import re
match = re.search(re_expr, html)
if not match:
    print('Не получилось вытащить описание модели')
    quit()

# Вытаскиваем объект js из параметра функции init
json_text = match.group(1)

# Парсим его как JSON
import json
json_data = json.loads(json_text)

# Вытаскиваем список ссылок на картинки
for url_img_rel in json_data['getImages']['originImg']:
    from urllib.parse import urljoin
    url_img = urljoin('http://gepur.ru', url_img_rel)

    print(url_img)
