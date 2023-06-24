#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://ru.stackoverflow.com/questions/854015/
"""
Пишу метод, который бы брал на вход словарь, проверял, хранятся ли ключи в значениях других ключей, 
если да - объединял бы оба списка значений. 
"""


total = {"a": ["b", "d"], "b": ["c", "d"], "c": ["d"]}

for k in total:
    for k1, v1 in total.items():
        if k == k1 or v1 is None or k not in v1:
            continue

        # Объединение значений
        total[k1] += total[k]

        # Обнуление значения у поглощенного ключа
        total[k] = None


print(total)  # {'a': ['b', 'd', 'c', 'd', 'd'], 'b': None, 'c': None}

total = {k: v for k, v in total.items() if v is not None}
print(total)  # {'a': ['b', 'd', 'c', 'd', 'd']}
