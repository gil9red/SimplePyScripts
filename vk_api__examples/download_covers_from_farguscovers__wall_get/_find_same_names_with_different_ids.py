#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import sys

from collections import defaultdict
from main import FILE_NAME_DUMP


if not FILE_NAME_DUMP.exists():
    print(f'Файл {FILE_NAME_DUMP.name!r} не найден, попробуй запустить main.py')
    sys.exit()

dumps = json.load(open(FILE_NAME_DUMP, encoding='utf-8'))

name_by_ids = defaultdict(set)
for dump in dumps:
    if 'authors' not in dump:
        continue

    for author in dump['authors']:
        name = author["name"]
        name_by_ids[name].add(author['id'])

print('Дубликаты:')
for name, ids in name_by_ids.items():
    if len(ids) == 1:
        continue

    print(f'{name}: {", ".join(map(str, sorted(ids)))}')
# DELETED: 74388128, 135225390, 230625225
