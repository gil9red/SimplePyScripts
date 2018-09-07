#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых игр серии Saga of the Nine Worlds.

"""


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')

# Чтобы импортировать функцию для получения списка игр
sys.path.append('../../bigfishgames_com__hidden_object')

from all_common import make_backslashreplace_console, get_logger, run_notification_job
from find__Saga_of_the_Nine_Worlds__CE import get_games


make_backslashreplace_console()


run_notification_job(
    'new game Saga of the Nine Worlds',
    'games',
    get_games,
    notified_by_sms=True,
    format_current_items='Текущий список игр (%s): %s',
    format_get_items='Запрос списка игр',
    format_items='Список игр (%s): %s',
    format_new_item='Появилась новая игра "%s"',
    format_no_new_items='Новых игр нет',
)
