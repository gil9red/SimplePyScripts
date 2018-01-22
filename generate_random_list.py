#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import random

# Non-Unique Numbers
items = [random.randint(0, 100000) for i in range(100000)]
print(len(items), items[:5])

# Unique Numbers
items = list(range(100000))
random.shuffle(items)
print(len(items), items[:5])
