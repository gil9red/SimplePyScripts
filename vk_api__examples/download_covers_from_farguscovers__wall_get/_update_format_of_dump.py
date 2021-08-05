#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import sys

from main import DIR, FILE_NAME_DUMP


if not FILE_NAME_DUMP.exists():
    print(f'Файл {FILE_NAME_DUMP.name!r} не найден, попробуй запустить main.py')
    sys.exit()

dump = json.load(open(FILE_NAME_DUMP, encoding='utf-8'))

need_update = False
for x in dump:
    x['game_series'] = ''
    for author in x['authors']:
        if 'url' in author:
            author.pop('url')
            need_update = True

        author_id = author['id']
        if isinstance(author_id, str):
            author['id'] = int(author_id[2:])
            need_update = True

if need_update:
    print('Дамп нужно обновить')
    json.dump(
        dump, open(FILE_NAME_DUMP, 'w', encoding='utf-8'),
        indent=4, ensure_ascii=False
    )
else:
    print('Дамп обновлять не нужно')
