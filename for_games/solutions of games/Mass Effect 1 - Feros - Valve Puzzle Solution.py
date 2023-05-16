#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import itertools


ITEMS = [5, 7, 17, 11, 13]
NEEDS = [31, 32, 33, 34]


for i in range(len(ITEMS)):
    for items in itertools.combinations(ITEMS, r=i + 1):
        total = sum(items)
        if total in NEEDS:
            print(f'{" + ".join(map(str, items))} = {total}')

"""
5 + 17 + 11 = 33
7 + 11 + 13 = 31
"""
