#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


text = 'a1b2c3d4f5'
result = [a + b for a, b in list(zip(text[::2], text[1::2]))]
print(result)  # ['a1', 'b2', 'c3', 'd4', 'f5']
