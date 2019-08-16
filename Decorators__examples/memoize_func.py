#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Using memoization as decorator (decorator-function)
def memoize_func(f):
    memo = dict()

    def func(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]

    return func


@memoize_func
def fib(n):
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a


print(fib(1000))
