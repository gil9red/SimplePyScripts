#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://www.delftstack.com/howto/python/python-pascal-triangle/#print-pascal-s-triangle-by-computing-the-power-of-11-in-python

"""
Print Pascal’s Triangle by Computing the Power of 11 in Python
"""


N = 5  # NOTE: MAXIMUM
for n in range(N):
    print(list(map(int, str(11 ** n))))
