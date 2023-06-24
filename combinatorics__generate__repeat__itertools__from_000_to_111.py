#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import itertools


items = ["".join(i) for i in itertools.product("01", repeat=3)]
print(items)  # ['000', '001', '010', '011', '100', '101', '110', '111']

items = [i for i in items if "11" not in i]
print(items)  # ['000', '001', '010', '100', '101']
