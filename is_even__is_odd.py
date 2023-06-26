#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def is_even(num):
    return num % 2 == 0


def is_odd(num):
    return not is_even(num)


def is_even_2(num):
    return num & 1 == 0


if __name__ == "__main__":
    for i in range(10):
        print(f"{i} is even: {is_even(i)}, {is_even_2(i)}")
        print(f"{i} is odd: {is_odd(i)}")
        print()
