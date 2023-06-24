#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
import numpy


number = 100000

#
# Non-Unique Numbers
#
items = [random.randint(0, 100000) for i in range(number)]
print(len(items), items[:5])  # 100000 [92560, 5867, 81098, 98309, 97995]

items = numpy.random.randint(100000, size=number)
print(len(items), items[:5])  # 100000 [73846 49707 18846 73887 43349]

#
# Unique Numbers
#
items = list(range(number))
random.shuffle(items)
print(len(items), items[:5])  # 100000 [36174, 38829, 93415, 74347, 40457]

items = numpy.random.choice(100000, number, replace=False)
print(len(items), items[:5])  # 100000 [94792 79537  9678 66784 92049]
