#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import json
import sys

from main import FILE_NAME_DUMP, get_wall_it


if not FILE_NAME_DUMP.exists():
    print(f'Файл {FILE_NAME_DUMP.name!r} не найден, попробуй запустить main.py')
    sys.exit()

dump = json.load(open(FILE_NAME_DUMP, encoding='utf-8'))
id_by_dump = {x['post_id']: x for x in dump}

for post in get_wall_it():
    post_id = post['id']
    if post_id not in id_by_dump:
        continue

    date_time = DT.datetime.fromtimestamp(post['date'])
    id_by_dump[post_id]['date_time'] = str(date_time)

print('Дамп перезаписан')

json.dump(
    dump, open(FILE_NAME_DUMP, 'w', encoding='utf-8'),
    indent=4, ensure_ascii=False
)
