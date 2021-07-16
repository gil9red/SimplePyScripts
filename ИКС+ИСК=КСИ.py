#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://stepik.org/lesson/360560/step/11?unit=345000


"""
Напишите программу, которая выводит решение ребуса ИКС+ИСК=КСИ. 
Одинаковым буквам соответствуют одинаковые цифры. 
Разным буквам соответствуют разные цифры. ИКС, ИСК, КСИ -- трехзначные числа. 
Числа не могут начинаться с нуля.
"""

for i in range(10):
    for k in range(10):
        for s in range(10):
            # Разным буквам соответствуют разные цифры
            if len({i, k, s}) != 3:
                continue

            iks = i * 100 + k * 10 + s
            isk = i * 100 + s * 10 + k
            ksi = k * 100 + s * 10 + i

            # Проверка, что числа трехзначные
            if any(n < 100 or n > 999 for n in [iks, isk, ksi]):
                continue

            if iks + isk == ksi:
                print(f'{iks}+{isk}={ksi}')
