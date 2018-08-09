#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


items = [1, 2, 0, 1, 3, 2]


seen = set()
print([x for x in items if x not in seen and not seen.add(x)])  # [1, 2, 0, 3]


from collections import OrderedDict
print(list(OrderedDict.fromkeys(items)))  # [1, 2, 0, 3]


# pip install more_itertools
from more_itertools import unique_everseen
print(list(unique_everseen(items)))  # [1, 2, 0, 3]
