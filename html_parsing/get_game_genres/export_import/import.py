#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json

import sys
sys.path.append('..')

from db import Dump

import peewee
from playhouse.shortcuts import dict_to_model

from export import FILE_NAME_EXPORT_JSON


items = json.load(
    open(FILE_NAME_EXPORT_JSON, encoding='utf-8')
)
print('items:', len(items))
print('Dump count before import:', Dump.select().count())

for x in items:
    try:
        dump = dict_to_model(Dump, x)
        dump.save(force_insert=True)
        print(f'Import {x}')

    except peewee.IntegrityError as e:
        # Ignore error "UNIQUE constraint failed: dump.id"
        pass

print('Current dump count:', Dump.select().count())
