#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""RU: Пример использования модуля copy."""

# TODO: https://docs.python.org/3.4/library/copy.html
# TODO: больше примеров


import copy


if __name__ == "__main__":
    a = [2, 3, [3.5, 3.6, [3.61, 3.62]], 4, 5]
    print(a, type(a), hex(id(a)), sep=", ")

    b = copy.deepcopy(a)
    print(b, type(b), hex(id(b)), sep=", ")

    c = [2, 3, 4, 5]
    print(c, type(c), hex(id(c)), sep=", ")

    d = copy.copy(c)
    print(d, type(d), hex(id(d)), sep=", ")
