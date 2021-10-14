#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/gil9red/SimplePyScripts/issues/13#issuecomment-943412289


"""
Напишите программу, которая выводит решение ребуса (K+U+B)^3=KUB, где знак ^ означает возведение в степень. 
Одинаковым буквам соответствуют одинаковые цифры. Разным буквам соответствуют разные цифры.
Выведите решение в формате (K+U+B)^3=KUB, где вместо букв подставлены цифры.
"""

for num in range(100, 1000):
    kub = set(str(num))
    if len(kub) == 3 and sum(map(int, kub))**3 == num:
        print(f'({"+".join(str(num))})^3={num}')
