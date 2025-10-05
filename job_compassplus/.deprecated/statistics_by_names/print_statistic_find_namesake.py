#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для поиска однофамильцев.

"""


from collections import defaultdict

# pip install pymorphy2
import pymorphy2

from print_statistic_all_names import get_all_names


name_list = get_all_names()
total = len(name_list)
print("Total:", total)
print()


morph = pymorphy2.MorphAnalyzer()


def get_normal_form(word):
    return morph.parse(word)[0].normal_form


second_name_by_full_name_list = defaultdict(list)

for name in name_list:
    second_name = name.split()[1]
    normal_form = get_normal_form(second_name)

    second_name_by_full_name_list[normal_form].append(name)

# Фильтр по однофамильцам
second_name_by_full_name_list = filter(
    lambda x: len(x[1]) > 1, second_name_by_full_name_list.items()
)

# Сортировка по количеству фамилий
second_name_by_full_name_list = sorted(
    second_name_by_full_name_list, key=lambda x: len(x[1]), reverse=True
)

# Вывод итоговых данных
for second_name, full_name_list in second_name_by_full_name_list:
    print(f"{second_name.upper()} ({len(full_name_list)}): {sorted(full_name_list)}")
