#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import re
import sqlite3

from collections import OrderedDict


def process_title(title: str) -> str:
    if title.startswith('Купить '):
        title = title[len('Купить '):]

    match = re.search('(.+?) – купить в интернет магазине DNS', title)
    if match:
        title = match.group(1)

    match = re.search('(.+?) в интернет магазине DNS', title)
    if match:
        title = match.group(1)

    return title


tracked_products = []

# C:\Users\<user>\AppData\Roaming\Mozilla\Firefox\Profiles\<profile>\places.sqlite
with sqlite3.connect('places.sqlite') as connect:
    sql = "select url, title from moz_places where title is not null and url like '%//www.dns-shop.ru/product/%/%/'"
    for url, title in connect.execute(sql):
        if not title:
            continue

        if url.startswith('http://'):
            url = 'https://' + url[len('http://'):]

        if not url.startswith('https://www.dns-shop.ru/product/'):
            continue

        if not re.fullmatch(r'https://www\.dns-shop\.ru/product/\w+/[^/]+/', url):
            continue

        title = process_title(title)
        print(url, title)

        tracked_products.append(
            OrderedDict([
                ('title', title),
                ('url', url),
            ])
        )

tracked_products.sort(key=lambda x: x['title'])

json.dump(
    tracked_products,
    open('tracked_products.json', 'w', encoding='utf-8'),
    indent=4, ensure_ascii=False
)
