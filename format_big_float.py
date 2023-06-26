#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


value = 0.000175 / 100 * 30
print(value)  # 5.25e-05
print()

value_str = f"{value:.10f}"
print(value_str)  # '0.0000525000'
print(value_str.rstrip("0"))  # '0.0000525'

print(f"{value:f}")  # '0.000053'
