#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install simpleeval
from simpleeval import simple_eval


print(simple_eval("21 + 21"))  # 42
print(simple_eval("2 + 2 * 2"))  # 6
print(simple_eval("10 ** 123"))  # 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
print(simple_eval("21 + 19 / 7 + (8 % 3) ** 9"))  # 535.7142857142857
print(simple_eval("square(11)", functions={"square": lambda x: x * x}))  # 121
