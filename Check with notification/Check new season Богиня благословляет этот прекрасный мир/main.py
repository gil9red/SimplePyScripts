#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых сезонов аниме "Богиня благословляет этот прекрасный мир".

"""


import re
import sys

from typing import List

import requests

# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
sys.path.append('..')
from all_common import make_backslashreplace_console, run_notification_job


def get_items() -> List[str]:
    rs = requests.get('https://en.wikipedia.org/wiki/List_of_KonoSuba_episodes')
    items = re.findall(r'Season \d+', rs.text)
    return sorted(set(items))


run_notification_job(
    'Новый сезон "Богиня благословляет этот прекрасный мир"',
    'seasons',
    get_items,
    notified_by_sms=True,
    format_current_items='Текущий список сезонов (%s): %s',
    format_get_items='Запрос сезонов',
    format_items='Список сезонов (%s): %s',
    format_new_item='Новый сезон "%s"',
    format_no_new_items='Изменений нет',
)
