#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json

import sys
sys.path.append('..')

from db import Dump
from load import FILE_NAME_GENRE_TRANSLATE, load
from utils_dump import get_logger


log = get_logger('genre_translate.txt')

log.info('Start.')
log.info('Load genres')

genre_translate = load()

log.info(f'Current genres: {len(genre_translate)}')

for genre in Dump.get_all_genres():
    if genre not in genre_translate:
        log.info(f'Added new genre: {genre!r}')
        genre_translate[genre] = None

log.info('Save genres')

json.dump(
    genre_translate,
    open(FILE_NAME_GENRE_TRANSLATE, 'w', encoding='utf-8'),
    ensure_ascii=False,
    indent=4
)

log.info('Finish!')
