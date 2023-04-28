#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Using memoization as decorator (decorator-class)
class MemoizeClass:
    def __init__(self, func):
        self.func = func
        self.memo = dict()

    def __call__(self, *arg):
        if arg not in self.memo:
            self.memo[arg] = self.func(*arg)

        return self.memo[arg]


@MemoizeClass
def fib(n):
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a


print(fib(1000))
