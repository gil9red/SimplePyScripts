#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""RU: Пример использования модуля copy."""


import copy


complex_data = [
    2,
    3,
    [
        3.5,
        3.6,
        [3.61, 3.62],
    ],
    dict(
        a=1,
        b="2",
        c=[True, None],
    ),
    4,
    5,
]


def _print_complex_data(data):
    print(data, id(data))
    print(data[2], id(data[2]))
    print(data[2][2], id(data[2][2]))
    print(data[3], id(data[3]))
    print(data[3]["c"], id(data[3]["c"]))


_print_complex_data(complex_data)
print()

_print_complex_data(copy.copy(complex_data))
print()

_print_complex_data(copy.deepcopy(complex_data))
