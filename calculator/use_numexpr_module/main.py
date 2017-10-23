#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import numexpr as ne
print(ne.evaluate('2 + 2 * 2'))
print(ne.evaluate('10 ** 3'))
print(ne.evaluate('2 ** 10'))
print(ne.evaluate('sin(2 ** 10)'))
print(ne.evaluate('(0xFF + 255) / 0b1010'))
print(ne.evaluate('(0xFF + 255) // 0b1010'))
