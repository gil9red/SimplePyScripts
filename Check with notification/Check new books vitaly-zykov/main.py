#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых книг Зыкова.

"""


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')

# Чтобы импортировать функцию для получения списка книг
sys.path.append('../../html_parsing')

from all_common import make_backslashreplace_console, run_notification_job
from vitaly_zykov_ru_knigi__get_books import get_books


make_backslashreplace_console()


run_notification_job(
    'vitaly-zykov new books',
    'books',
    get_books,
    notified_by_sms=True,
    format_current_items='Текущий список книг (%s): %s',
    format_get_items='Запрос списка книг',
    format_items='Список книг (%s): %s',
    format_new_item='Появилась новая книга Зыкова: "%s"',
    format_no_new_items='Новых книг нет',
)
