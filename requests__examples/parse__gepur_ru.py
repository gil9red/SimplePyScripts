#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import sys
import re

from urllib.parse import urljoin

import requests


session = requests.session()
rs = session.get('http://gepur.ru/product/plate-6917')
html = rs.text

# Ищем следующую строку c описанием модели
match = re.search(r'ProductPage\.init\((.+)\)', html)
if not match:
    print('Не получилось вытащить описание модели')
    sys.exit()

# Вытаскиваем объект js из параметра функции init
json_text = match.group(1)

# Парсим его как JSON
json_data = json.loads(json_text)

# Вытаскиваем список ссылок на картинки
for url_img_rel in json_data['getImages']['originImg']:
    url_img = urljoin('http://gepur.ru', url_img_rel)
    print(url_img)
