#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install fuzzywuzzy[speedup]
from fuzzywuzzy import fuzz


print(fuzz.ratio("Hello World!", "Hello World!"))
# 100

print(fuzz.ratio("Hello World", "Hello World!"))
# 96

print(fuzz.ratio("HELLO WORLD!", "Hello World!"))
# 33

print(fuzz.ratio("HELLO WORLD!".lower(), "Hello World!".lower()))
# 100

print(fuzz.token_set_ratio("HELLO WORLD!", "Hello World!"))
# 100

print(fuzz.token_set_ratio("HELLO   WORLD", "Hello World!"))
# 100

print(fuzz.token_set_ratio("HELLO   WOR  LD", "Hello World!"))
# 78
