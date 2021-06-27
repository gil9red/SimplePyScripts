#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import sys

from pathlib import Path

DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = DIR.parent.parent

sys.path.append(str(DIR))
sys.path.append(str(ROOT_DIR))

from db import Dump
from load import FILE_NAME_GENRE_TRANSLATE, load
from common_utils import get_logger
from telegram_notifications.add_notify import add_notify


log = get_logger('genre_translate.txt')


def run(need_notify=True):
    log.info('Start load genres.')

    genre_translate = load()
    is_first_run = not genre_translate

    log.info(f'Current genres: {len(genre_translate)}')

    new_genres = []
    for genre in Dump.get_all_genres():
        if genre not in genre_translate:
            log.info(f'Added new genre: {genre!r}')
            genre_translate[genre] = None
            new_genres.append(genre)

    if new_genres:
        text = f"Added genres ({len(new_genres)}): {', '.join(new_genres)}"
        log.info(text)

        # Если это первый запуск, то смс не отправляем
        if not is_first_run and need_notify:
            add_notify(log.name, text)

        log.info('Save genres')

        json.dump(
            genre_translate,
            open(FILE_NAME_GENRE_TRANSLATE, 'w', encoding='utf-8'),
            ensure_ascii=False,
            indent=4
        )

    else:
        log.info('No new genres')

    log.info('Finish!')


if __name__ == '__main__':
    run()
