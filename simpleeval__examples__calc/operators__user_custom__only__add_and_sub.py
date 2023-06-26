#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/danthedeckie/simpleeval#operators


import ast
import operator as op

# pip install simpleeval
from simpleeval import simple_eval, SimpleEval


SUPPORTED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
}


print(simple_eval("2 + 2 - 1", operators=SUPPORTED_OPERATORS))
# 3

try:
    print(
        simple_eval("2 + 2 * 2", operators=SUPPORTED_OPERATORS)
    )
    # KeyError: <class '_ast.Mult'>
except Exception as e:
    print(repr(e))

print()

s = SimpleEval(operators=SUPPORTED_OPERATORS)
# # OR:
# s = SimpleEval()
# s.operators = SUPPORTED_OPERATORS

print(s.eval("2 + 2 - 1"))  # 3

try:
    print(s.eval("2 + 2 * 2"))  # KeyError: <class '_ast.Mult'>
except Exception as e:
    print(repr(e))
