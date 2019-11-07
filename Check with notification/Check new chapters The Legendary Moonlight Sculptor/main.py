#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых главах Легендарного лунного скульптора.

"""


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')

# Чтобы импортировать функцию для получения списка глав
sys.path.append('../../html_parsing')

from all_common import make_backslashreplace_console, run_notification_job
from ranobehub_org_api_ranobe_92_contents__The_Legendary_Moonlight_Sculptor import get_chapters


make_backslashreplace_console()


run_notification_job(
    'New chapters The Legendary Moonlight Sculptor',
    'chapters',
    get_chapters,
    notified_by_sms=True,
    format_current_items='Текущий список глав (%s): %s',
    format_get_items='Запрос списка глав',
    format_items='Список глав (%s): %s',
    format_new_item='Появилась новая глава Легендарного лунного скульптора: "%s"',
    format_no_new_items='Новых глав нет',
)
