#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
sys.path.append('..')

# Для импортирования kanobu_ru__games__collections__igry_s_podderzhkoi_rtx.py
sys.path.append('../../html_parsing')

from all_common import get_logger, wait, simple_send_sms
from kanobu_ru__games__collections__igry_s_podderzhkoi_rtx import get_games
from db import db_create_backup, Game


log = get_logger(__file__)


while True:
    log.debug('Запуск')

    is_empty = not Game.select().count()
    if is_empty:
        log.debug('Обнаружен первый запуск')
    else:
        db_create_backup()

    try:
        has_new_game = False

        games = get_games()
        log.debug(f'Обработка {len(games)} игр')

        for game in games:
            game_db, created = Game.get_or_create(
                name=game.name,
                url=game.url
            )
            if game_db.img_base64 != game.img_base64:
                game_db.img_base64 = game.img_base64
                game_db.save()

            if not created:
                continue

            has_new_game = True
            log.debug(f'Добавление новой игры с RTX: {game.name!r}')

            # При первом запуске не нужно информировать по СМС
            if not is_empty:
                simple_send_sms(f'RTX: {game.name}', log)

        if not has_new_game:
            log.debug(f'Новых игр нет')

        wait(weeks=1)

    except Exception as e:
        log.exception('Ошибка:')

        wait(minutes=15)

    print()
