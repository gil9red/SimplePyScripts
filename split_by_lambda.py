#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from itertools import groupby


items = '123-456-789'

parts = [list(x[1]) for x in groupby(items, lambda x: x == '-') if not x[0]]
print(parts)
# [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
