#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import timeit


number = 10000

print(
    timeit.timeit(
        """
text = ''
for _ in range(1000):
    text += 'abc'
    """,
        number=number,
    )
)

print(
    timeit.timeit(
        """
text = []
for _ in range(1000):
    text.append('abc')
    
text = ''.join(text)
    """,
        number=number,
    )
)

print(timeit.timeit("text = ''.join('abc' for _ in range(1000))", number=number))

print(timeit.timeit("text = ''.join(['abc' for _ in range(1000)])", number=number))
