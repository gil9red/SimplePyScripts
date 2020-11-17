#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

a, oper, b = sys.argv[1:]
a = float(a)
b = float(b)
if oper == '+':
    print(a + b)
else:
    print(f'Not supported {oper!r}')
