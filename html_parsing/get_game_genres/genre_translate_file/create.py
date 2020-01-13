#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json

import sys
sys.path.append('..')

from db import Dump
from load import FILE_NAME_GENRE_TRANSLATE, load
from common_utils import get_logger
from utils import send_sms


log = get_logger('genre_translate.txt')


def run():
    log.info('Start load genres.')

    genre_translate = load()

    NEED_SMS = True
    number = 0
    is_first_run = not genre_translate

    log.info(f'Current genres: {len(genre_translate)}')

    for genre in Dump.get_all_genres():
        if genre not in genre_translate:
            log.info(f'Added new genre: {genre!r}')
            genre_translate[genre] = None
            number += 1

    if number:
        log.info(f"Added {number} genre(s)")
    else:
        log.info('No new genres')

    # Если это первый запуск, то смс не отправляем
    if not is_first_run:
        if NEED_SMS and number:
            send_sms(f"Added {number} genre(s)", log=log)

    log.info('Save genres')

    json.dump(
        genre_translate,
        open(FILE_NAME_GENRE_TRANSLATE, 'w', encoding='utf-8'),
        ensure_ascii=False,
        indent=4
    )

    log.info('Finish!')


if __name__ == '__main__':
    run()
