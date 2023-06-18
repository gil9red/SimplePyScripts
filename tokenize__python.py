#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import token
import tokenize

from io import StringIO


prog_example = """
for i in range(100): # comment
    if i % 1 == 0: 
        print(":", t**2)
"""

rl = StringIO(prog_example).readline

for t_type, t_str, (br, bc), (er, ec), logl in tokenize.generate_tokens(rl):
    print("%3i %10s : %20r" % (t_type, token.tok_name[t_type], t_str))
