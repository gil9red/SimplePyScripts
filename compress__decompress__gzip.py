#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import gzip


s_in = "HelloWorld!" * 1000000
s_in = bytes(s_in, encoding="utf-8")
print(len(s_in))  # 11000000

s_out = gzip.compress(s_in)
assert gzip.decompress(s_out) == s_in
print(len(s_out))  # 21396
