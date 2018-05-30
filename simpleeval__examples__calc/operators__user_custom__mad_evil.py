#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/danthedeckie/simpleeval#operators


# pip install simpleeval
from simpleeval import SimpleEval

import ast
import operator


expr = "((2 + 2 * 2) / 3) ** 10 - 24"

s = SimpleEval()
print(s.eval(expr))  # 1000.0

# Mad
s.operators[ast.Add] = operator.mul
s.operators[ast.Sub] = operator.add
s.operators[ast.Mult] = operator.pow
s.operators[ast.Pow] = operator.sub

print(s.eval(expr))  # 16.666666666666664
