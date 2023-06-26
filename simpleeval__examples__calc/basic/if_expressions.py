#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/danthedeckie/simpleeval/blob/master/README.rst#if-expressions


# pip install simpleeval
from simpleeval import simple_eval


# You can use python style if x then y else z type expressions:
print(
    simple_eval("'equal' if x == y else 'not equal'", names={"x": 1, "y": 2})
)
# 'not equal'

print(
    simple_eval("'equal' if x == y else 'not equal'", names={"x": 1, "y": 1})
)
# 'equal'

# which, of course, can be nested:
print(simple_eval("'a' if 1 == 2 else 'b' if 2 == 3 else 'c'"))  # 'c'
