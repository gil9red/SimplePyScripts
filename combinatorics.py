#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
У нас есть список сил и возможно комбинировать одновременно только две разные силы,
причем повторов быть не должно -- ('Огонь', 'Молния') и ('Молния', 'Огонь') -- повторы.
"""


import itertools


# Комбинации сил, максимум за раз могут две учавствовать, плюс возможны только разные
powers = ["Огонь", "Молния", "Лед", "Воздух"]

# Все комбинации без повторов
# Если нужны комбинации с повторами, используется itertools.product(powers, repeat=2)
all_combo = itertools.combinations(powers, 2)
for i, combo in enumerate(all_combo, 1):
    print("{}. {} и {}".format(i, *combo))
