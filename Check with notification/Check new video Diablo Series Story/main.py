#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео истории серии Diablo.

"""


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')

# Чтобы импортировать функцию для получения списка видео
sys.path.append('../../html_parsing')

from all_common import make_backslashreplace_console, run_notification_job
from youtube_com__get_video_list import get_video_list


make_backslashreplace_console()


def my_get_video_list():
    text = 'История серии Diablo'
    url = 'https://www.youtube.com/user/StopGameRu/search?query=' + text

    return get_video_list(url, filter_func=lambda name: text.lower() in name.lower())


if __name__ == '__main__':
    run_notification_job(
        'Check new video Diablo Series Story',
        'video',
        my_get_video_list,
        notified_by_sms=True,
        format_current_items='Текущий список видео (%s): %s',
        format_get_items='Запрос видео',
        format_items='Список видео (%s): %s',
        format_new_item='Новое видео "%s"',
        format_no_new_items='Изменений нет',
    )
