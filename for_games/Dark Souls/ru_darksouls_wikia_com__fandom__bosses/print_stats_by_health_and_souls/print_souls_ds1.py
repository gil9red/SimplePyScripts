#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from _utils import parse, print_stats, URL_DS1


print(URL_DS1)
rows = parse(URL_DS1)
print_stats(rows, sort_column=2)
"""
https://darksouls.fandom.com/ru/wiki/Боссы
NAME                    | HEALTH | SOULS
------------------------+--------+------
Гвин Повелитель Пепла   | 4250   | 70000
Ложе Хаоса              | 14     | 60000
Нагой Сит               | 6355   | 60000
Четыре Короля           | 9504   | 60000
Нито Повелитель Могил   | 4300   | 60000
Манус Отец Бездны       | 6666   | 60000
Черный дракон Каламит   | 5940   | 60000
Орнштейн и Смоуг        | 4286   | 50000
Арториас Путник Бездны  | 3750   | 50000
Сиф Великий Волк        | 3432   | 40000
Железный голем          | 2923   | 40000
Демон-стоног            | 3432   | 40000
Гвиндолин Темное Солнце | 2000   | 40000
Присцилла Полукровка    | 2458   | 30000
Страж Святилища         | 3060   | 30000
Разверстый Дракон       | 4401   | 25000
Квилег Ведьма Хаоса     | 3139   | 20000
Бродячий Демон          | 5250   | 20000
Неутомимый воин         | 4200   | 20000
Мудрый демон Огня       | 5448   | 20000
Вихрь                   | 1326   | 15000
Горгулья                | 1479   | 10000
Лунная Бабочка          | 1506   | 10000
Демон Капра             | 1176   | 6000 
Демон-Телец             | 1250   | 3000 
Демон Прибежища         | 813    | 2000 
"""
