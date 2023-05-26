#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import inspect


print("Current line:", inspect.getframeinfo(inspect.currentframe()).lineno)
print("Current line:", inspect.getframeinfo(inspect.currentframe()).lineno)
print("Current line:", inspect.getframeinfo(inspect.currentframe()).lineno)
print()

print("Current filename:", inspect.getframeinfo(inspect.currentframe()).filename)
print()

print(
    "Current code context:", inspect.getframeinfo(inspect.currentframe()).code_context
)
print()

print("Current function:", inspect.getframeinfo(inspect.currentframe()).function)
print(
    "Current function:",
    (lambda: inspect.getframeinfo(inspect.currentframe()).function)(),
)


def foo():
    return inspect.getframeinfo(inspect.currentframe()).function


print("Current function:", foo())
