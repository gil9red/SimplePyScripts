#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


items = [5, 80, 3, 83, 1, 77, 1, 77, 2, 82, 1, 77, 5, 81, 2, 78, 1, 81, 5, 85, 5, 85, 4, 84, 2, 78, 1, 81, 3, 83]

new_items = [(items[i], items[i + 1]) for i in range(0, len(items), 2)]
print(new_items)  # [(5, 80), (3, 83), (1, 77), (1, 77), (2, 82), ...

new_items = [x for x in zip(*[iter(items)] * 2)]
print(new_items)  # [(5, 80), (3, 83), (1, 77), (1, 77), (2, 82), ...
