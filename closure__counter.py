#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://stackoverflow.com/a/141426


def make_counter(start=0, step=1):
    i = start

    def counter():  # counter() is a closure
        nonlocal i
        i += step

        return i

    return counter


if __name__ == '__main__':
    c1 = make_counter()
    print(c1(), c1(), c1())  # 1 2 3

    c2 = make_counter(step=0.1)
    print(c2(), c2(), c2())  # 0.1 0.2 0.30000000000000004
