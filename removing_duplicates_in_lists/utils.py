#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists


from collections import OrderedDict
from functools import reduce

# pip install pandas
import pandas as pd

# pip install numpy
import numpy as np


def remove_duplicates__list_set(items: list) -> list:
    return list(set(items))


def remove_duplicates__OrderedDict_fromkeys(items: list) -> list:
    return list(OrderedDict.fromkeys(items))


def remove_duplicates__dict_fromkeys(items: list) -> list:
    return list(dict.fromkeys(items))


def remove_duplicates__OrderedDict_list_v1(items: list) -> list:
    return list(OrderedDict((x, True) for x in items))


def remove_duplicates__OrderedDict_list_v2(items: list) -> list:
    return list(OrderedDict((x, True) for x in items).keys())


def remove_duplicates__generate_new_list_v1(items: list) -> list:
    out_list = []
    added = set()
    for val in items:
        if val not in added:
            out_list.append(val)
            added.add(val)
    return out_list


def remove_duplicates__generate_new_list_v2(items: list) -> list:
    return [x for i, x in enumerate(items) if x not in items[:i]]


# SOURCE: https://stackoverflow.com/a/29898868/5909792
def remove_duplicates__reduce_v1(items: list) -> list:
    return reduce(lambda r, v: v in r and r or r + [v], items, [])


# SOURCE: https://stackoverflow.com/a/29898868/5909792
def remove_duplicates__reduce_v2(items: list) -> list:
    return reduce(
        lambda r, v: v in r[1] and r or (r[0].append(v) or r[1].add(v)) or r,
        items,
        ([], set()),
    )[0]


def remove_duplicates__pandas(items: list) -> list:
    return pd.unique(items).tolist()


def remove_duplicates__numpy(items: list) -> list:
    return np.unique(items).tolist()


# Найдем все функции из этого файла по их названию
ALL_EXAMPLE_FUNC_REMOVE_DUPLICATES = [
    globals()[name] for name in sorted(dir()) if name.startswith("remove_duplicates")
]
