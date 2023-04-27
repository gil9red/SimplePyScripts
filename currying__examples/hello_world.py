#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.wikipedia.org/wiki/Каррирование


def my_sum(x, y, z):
    return x + y + z


def foo(x):
    def a(y):
        def b(z):
            return my_sum(x, y, z)

        return b

    return a


print(foo(1)(2)(3))  # 6
print(foo("1")("2")("3"))  # 123
