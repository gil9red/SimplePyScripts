#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re

import requests


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'

session = requests.session()
session.headers['User-Agent'] = USER_AGENT


def get_url_img(media: dict) -> str:
    # Example: https://arthive.net/res/media/img/orig/work/0f0/611262.webp
    return f"{media['base_url']}/img/orig/work/{media['data']['version_orig']}/{media['media_id']}.webp"


rs = session.get('https://artchive.ru/hansruedigiger/works')
rs.raise_for_status()

m = re.search(r' artist_id="(\d+)"', rs.text)
if not m:
    raise Exception('Not found artist_id!')

artist_id = m.group(1)

url_api = f'https://artchive.ru/action/vue/works/search'
params = {
    'p': 1,
    'artist': artist_id,
}

rs = session.get(url_api, params=params)
rs.raise_for_status()

data = rs.json()

for work in data['works']:
    url_img = get_url_img(work['media'])
    print(work['name'])
    print(url_img)
    print()
"""
Чужой - Иероглифика
https://arthive.net/res/media/img/orig/work/0f0/611262.webp

Чужой - монстр
https://arthive.net/res/media/img/orig/work/520/602973.webp

Альфа
https://arthive.net/res/media/img/orig/work/250/611263.webp

...

Биомеханический гуманоид
https://arthive.net/res/media/img/orig/work/efb/611280.webp
"""
