#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для поиска однофамильцев.

"""


from print_statistic_all_names import get_all_names
name_list = get_all_names()
total = len(name_list)
print('Total:', total)
print()

from collections import defaultdict
second_name_by_full_name_list = defaultdict(list)

# pip install pymorphy2
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def get_normal_form(word):
    return morph.parse(word)[0].normal_form


for name in name_list:
    second_name, _, _ = name.split()
    normal_form = get_normal_form(second_name)

    second_name_by_full_name_list[normal_form].append(name)

# Фильтр по однофамильцам
second_name_by_full_name_list = filter(lambda x: len(x[1]) > 1, second_name_by_full_name_list.items())

# Сортировка по количеству фамилий
second_name_by_full_name_list = sorted(second_name_by_full_name_list, key=lambda x: len(x[1]), reverse=True)

# Вывод итоговых данных
for second_name, full_name_list in second_name_by_full_name_list:
    print('{} ({}): {}'.format(second_name.upper(), len(full_name_list), sorted(full_name_list)))
