#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import numexpr


print(numexpr.evaluate("2 + 2 * 2"))
print(numexpr.evaluate("10 ** 3"))
print(numexpr.evaluate("2 ** 10"))
print(numexpr.evaluate("sin(2 ** 10)"))
print(numexpr.evaluate("(0xFF + 255) / 0b1010"))
print(numexpr.evaluate("(0xFF + 255) // 0b1010"))
