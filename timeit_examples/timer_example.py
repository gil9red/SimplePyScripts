#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Performance Measurement (модуль timeit_example)
from timeit import Timer


print(Timer("t=a; a=b; b=t", "a=1; b=2").timeit())
print(Timer("a,b = b,a", "a=1; b=2").timeit())
