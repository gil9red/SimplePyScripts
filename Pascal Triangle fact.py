#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import math


N = 8
for n in range(N+1):
    print(n, [math.factorial(n) // (math.factorial(m) * math.factorial(n - m)) for m in range(n+1)])
