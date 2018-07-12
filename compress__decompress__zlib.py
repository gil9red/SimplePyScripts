#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


s_in = "HelloWorld!" * 1000000
s_in = bytes(s_in, encoding='utf-8')
print(len(s_in))  # 11000000

import zlib
s_out = zlib.compress(s_in)
assert zlib.decompress(s_out) == s_in
print(len(s_out))  # 21384
