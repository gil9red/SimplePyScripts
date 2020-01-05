#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json


FILE_NAME_GENRE_TRANSLATE = 'genre_translate.json'


def load(file_name: str = FILE_NAME_GENRE_TRANSLATE) -> dict:
    try:
        genre_translate = json.load(
            open(file_name, encoding='utf-8')
        )
    except:
        genre_translate = dict()

    return genre_translate


if __name__ == '__main__':
    genre_translate = load()
    print(genre_translate)
