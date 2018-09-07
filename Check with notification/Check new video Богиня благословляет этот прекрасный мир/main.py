#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых серий аниме Богиня благословляет этот прекрасный мир.

"""


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')

# Чтобы импортировать функцию для получения списка видео
sys.path.append('../../online_anidub_com')

from all_common import make_backslashreplace_console, run_notification_job
from get_video_list import search_video_list


make_backslashreplace_console()


run_notification_job(
    'new video Богиня благословляет этот прекрасный мир',
    'video',
    lambda: search_video_list('Богиня благословляет этот прекрасный мир'),
    notified_by_sms=True,
    timeout={'weeks': 2},
    format_current_items='Текущий список видео (%s): %s',
    format_get_items='Запрос видео',
    format_items='Список видео (%s): %s',
    format_new_item='Новая серия "%s"',
    format_no_new_items='Изменений нет',
)
