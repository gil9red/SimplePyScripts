#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/141426


def make_counter(start: int | float = 0, step: int | float = 1):
    i = start

    def counter():  # counter() is a closure
        nonlocal i
        i += step

        return i

    return counter


def make_counter_adder(start: int | float = 0):
    i = start

    def counter(step: int | float = 0):  # counter() is a closure
        nonlocal i
        i += step

        return i

    return counter


if __name__ == "__main__":
    c = make_counter()
    print(c(), c(), c())  # 1 2 3

    c = make_counter(step=0.1)
    print(c(), c(), c())  # 0.1 0.2 0.30000000000000004

    print()

    c = make_counter_adder()
    print(c(1), c(1), c(1))  # 1 2 3

    c = make_counter_adder(0.0)
    print(c(0.1), c(0.1), c(0.1))  # 0.1 0.2 0.30000000000000004
