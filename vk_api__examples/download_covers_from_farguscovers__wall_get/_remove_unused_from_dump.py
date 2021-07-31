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

new_dump = []
for x in dump:
    photo_file_name = x['photo_file_name']

    file_name = DIR / photo_file_name
    if file_name.exists():
        new_dump.append(x)
    else:
        print(f"Дамп с photo_file_name={photo_file_name} удален")

if len(new_dump) == len(dump):
    print('В дампе ничего не поменялось')
else:
    json.dump(
        new_dump, open(FILE_NAME_DUMP, 'w', encoding='utf-8'),
        indent=4, ensure_ascii=False
    )
