#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json


def dict_clean(items, default):
    return {
        k: default if v is None else v
        for k, v in items
    }


FILE_NAME_GENRE_TRANSLATE = 'genre_translate.json'


def load() -> dict:
    try:
        genre_translate = json.load(
            open(FILE_NAME_GENRE_TRANSLATE, encoding='utf-8'),
            object_pairs_hook=lambda items: dict_clean(items, default=[])
        )
    except:
        genre_translate = dict()

    return genre_translate


if __name__ == '__main__':
    genre_translate = load()
    print(genre_translate)
