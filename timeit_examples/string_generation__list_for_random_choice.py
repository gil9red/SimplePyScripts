#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import timeit


setup = """
from random import choices, choice
from string import ascii_letters
"""
number = 100

print(
    timeit.timeit(
        "[''.join(choices(ascii_letters, k=10)) for _ in range(1000)]",
        setup=setup,
        number=number,
    )
)

print(
    timeit.timeit(
        "[''.join([choice(ascii_letters) for _ in range(10)]) for _ in range(1000)]",
        setup=setup,
        number=number,
    )
)
