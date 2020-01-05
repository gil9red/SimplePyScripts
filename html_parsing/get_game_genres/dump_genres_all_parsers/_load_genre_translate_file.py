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
    print()

    # Print all undefined genres without '{' / '}' and indent
    genre_null_translate = {
        k: v
        for k, v in genre_translate.items()
        if v is None
    }
    json_text = json.dumps(genre_null_translate, ensure_ascii=False, indent=4)
    lines = json_text.splitlines()[1:-1]
    for i, line in enumerate(lines):
        print(line.strip())
        if i > 0 and i % 40 == 0:
            print()
