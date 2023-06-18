#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import io
import tokenize as T
from operator import itemgetter


# SOURCE: https://ru.stackoverflow.com/a/851992/201445
def tokenize_string(data):
    tokens = T.tokenize(io.BytesIO(data.strip().encode()).readline)
    next(tokens)  # skip encoding token
    return list(filter(None, map(itemgetter(1), tokens)))  # filter ENDMARKER


if __name__ == "__main__":
    print(tokenize_string("Myvar5:=arr[-10];"))
    # ['Myvar5', ':', '=', 'arr', '[', '-', '10', ']', ';']

    print(tokenize_string("x = 10 * 3"))  # ['x', '=', '10', '*', '3']
    print(tokenize_string("a = b + c"))  # ['a', '=', 'b', '+', 'c']
