#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/danthedeckie/simpleeval#operators


import ast
import operator as op

# pip install simpleeval
from simpleeval import SimpleEval


expr = "((2 + 2 * 2) / 3) ** 10 - 24"

s = SimpleEval()
print(s.eval(expr))  # 1000.0

# Mad
s.operators[ast.Add] = op.mul
s.operators[ast.Sub] = op.add
s.operators[ast.Mult] = op.pow
s.operators[ast.Pow] = op.sub

print(s.eval(expr))  # 16.666666666666664
