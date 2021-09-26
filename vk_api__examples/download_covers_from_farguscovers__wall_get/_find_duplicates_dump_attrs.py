#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import sys
import re

from collections import defaultdict

from main import DIR, FILE_NAME_DUMP, DIR_IMAGES


def clear_text(text: str) -> str:
    return re.sub(r'\W', '', text).lower()


if not FILE_NAME_DUMP.exists():
    print(f'Файл {FILE_NAME_DUMP.name!r} не найден, попробуй запустить main.py')
    sys.exit()

dumps = json.load(open(FILE_NAME_DUMP, encoding='utf-8'))

cover_text_by_duplicates = defaultdict(set)
game_name_by_duplicates = defaultdict(set)
game_series_by_duplicates = defaultdict(set)
for dump in dumps:
    cover_text = dump['cover_text']
    cover_text_by_duplicates[clear_text(cover_text)].add(cover_text)

    game_name = dump['game_name']
    game_name_by_duplicates[clear_text(game_name)].add(game_name)

    game_series = dump['game_series']
    game_series_by_duplicates[clear_text(game_series)].add(game_series)

print('Duplicates by cover_text:')
for cover_text, items in cover_text_by_duplicates.items():
    if len(items) > 1:
        print(f'    {cover_text!r}: {items}')

print()

print('Duplicates by game_name:')
for game_name, items in game_name_by_duplicates.items():
    if len(items) > 1:
        print(f'    {game_name!r}: {items}')

print()

print('Duplicates by game_series:')
for game_series, items in game_series_by_duplicates.items():
    if len(items) > 1:
        print(f'    {game_series!r}: {items}')
