#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())
items = sorted([int(input()) for i in range(n)])
# print(items, file=sys.stderr)

min_strength = items[0]
last = items[0]

for i in items[1:]:
    diff = abs(last - i)
    if diff < min_strength:
        min_strength = diff

    last = i

print(min_strength)
