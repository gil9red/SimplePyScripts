#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для анализа популярности имен и выдачи топа из имен.

Пример:
    Total: 409
    Top 15:
        Александр: 21 (5.1%)
        Дмитрий: 20 (4.9%)
        Сергей: 15 (3.7%)
        Алексей: 14 (3.4%)
        Елена: 14 (3.4%)
        Евгений: 14 (3.4%)
        Ольга: 12 (2.9%)
        Денис: 11 (2.7%)
        Андрей: 9 (2.2%)
        Ирина: 9 (2.2%)
        Владимир: 9 (2.2%)
        Илья: 9 (2.2%)
        Наталья: 9 (2.2%)
        Татьяна: 8 (2.0%)
        Максим: 8 (2.0%)

"""


from collections import Counter
from print_statistic_all_names import get_all_names


first_name_list = [name[1] for name in get_all_names(split_name=True)]
total = len(first_name_list)
print('Total:', total)
print()

print('Top 15:')
counter = Counter(first_name_list)

# Сортировка по количеству
for name, number in sorted(counter.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f'    {name}: {number} ({number * 100 / total:.1f}%)')
