#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/bz2.html#one-shot-de-compression


import bz2


s_in = "HelloWorld!" * 1000000
s_in = bytes(s_in, encoding="utf-8")
print(len(s_in))  # 11000000

s_out = bz2.compress(s_in)
assert bz2.decompress(s_out) == s_in
print(len(s_out))  # 927
