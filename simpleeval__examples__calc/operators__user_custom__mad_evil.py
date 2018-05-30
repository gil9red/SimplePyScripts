#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/danthedeckie/simpleeval#operators


# pip install simpleeval
from simpleeval import SimpleEval

import ast


expr = "((2 + 2 * 2) / 3) ** 10 - 24"

s = SimpleEval()
print(s.eval(expr))  # 1000.0

# Mad
s.operators[ast.Add] = lambda a, b: a * b
s.operators[ast.Sub] = lambda a, b: a + b
s.operators[ast.Mult] = lambda a, b: a ** b
s.operators[ast.Pow] = lambda a, b: a - b

print(s.eval(expr))  # 16.666666666666664
