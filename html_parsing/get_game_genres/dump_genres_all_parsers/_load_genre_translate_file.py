#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json


def dict_clean(items, default):
    return {
        k: default if v is None else v
        for k, v in items
    }


genre_translate = json.load(
    open('genre_translate.json', encoding='utf-8'),
    object_pairs_hook=lambda items: dict_clean(items, default=[])
)
print(genre_translate)
