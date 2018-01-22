#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import random

#
# Non-Unique Numbers
#
items = [random.randint(0, 100000) for i in range(100000)]
print(len(items), items[:5])  # 100000 [92560, 5867, 81098, 98309, 97995]

import numpy
items = numpy.random.random_integers(100000, size=100000)
print(len(items), items[:5])  # 100000 [73846 49707 18846 73887 43349]

#
# Unique Numbers
#
items = list(range(100000))
random.shuffle(items)
print(len(items), items[:5])  # 100000 [36174, 38829, 93415, 74347, 40457]
