#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Fresh values from:
# from print__stats_ds1 import get_stats_ds1
# from print__stats_ds2 import get_stats_ds2
# from print__stats_ds3 import get_stats_ds3
#
# stats_ds1 = [x[0] for x in get_stats_ds1()]
# stats_ds2 = [x[0] for x in get_stats_ds2()]
# stats_ds3 = [x[0] for x in get_stats_ds3()]

stats_ds1 = [
    "Вера",
    "Выносливость",
    "Живучесть",
    "Интеллект",
    "Ловкость",
    "Поиск предметов",
    "Сила",
    "Сопротивление",
    "Уровень",
    "Ученость",
    "Человечность",
]
stats_ds2 = [
    "Адаптируемость",
    "Вера",
    "Жизненная сила",
    "Интеллект",
    "Ловкость",
    "Сила",
    "Стойкость",
    "Уровень",
    "Ученость",
    "Физическая мощь",
]
stats_ds3 = [
    "Вера",
    "Жизненная сила",
    "Интеллект",
    "Ловкость",
    "Сила",
    "Стойкость",
    "Удача",
    "Уровень",
    "Ученость",
    "Физическая мощь",
]

stats_ds1 = set(stats_ds1)
stats_ds2 = set(stats_ds2)
stats_ds3 = set(stats_ds3)

common_stats = sorted(stats_ds1 & stats_ds2 & stats_ds3)
print(common_stats)  # ['Вера', 'Интеллект', 'Ловкость', 'Сила', 'Уровень', 'Ученость']
print()

unique_ds1 = sorted(stats_ds1 - stats_ds2 - stats_ds3)
print(unique_ds1)
# ['Выносливость', 'Живучесть', 'Поиск предметов', 'Сопротивление', 'Человечность']

unique_ds2 = sorted(stats_ds2 - stats_ds1 - stats_ds3)
print(unique_ds2)  # ['Адаптируемость']

unique_ds3 = sorted(stats_ds3 - stats_ds1 - stats_ds2)
print(unique_ds3)  # ['Удача']
