#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/lzma.html#lzma.compress


import lzma


s_in = "HelloWorld!" * 1000000
s_in = bytes(s_in, encoding="utf-8")
print(len(s_in))  # 11000000

s_out = lzma.compress(s_in)
assert lzma.decompress(s_out) == s_in
print(len(s_out))  # 1744
