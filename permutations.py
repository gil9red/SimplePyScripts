#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from itertools import permutations


items = list(permutations("abc", r=3))
print(items)
# [('a', 'b', 'c'), ('a', 'c', 'b'), ('b', 'a', 'c'), ('b', 'c', 'a'), ('c', 'a', 'b'), ('c', 'b', 'a')]

items = list(permutations("abc", r=2))
print(items)  # [('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')]
