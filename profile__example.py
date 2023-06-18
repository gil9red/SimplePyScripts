#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import profile


def foo(number=100):
    def _inc_i():
        nonlocal i
        i += 1

    def _has(value, items):
        return value in items

    items = ["1234567890" for _ in range(number)]
    print(items)

    i = 0

    for i in range(number):
        _inc_i()
        _has("5", items)

    print(i)


profile.run(r"foo(1000)")
# LOOK: 1000    0.016    0.000    0.016    0.000 profile__example.py:14(_has)
