#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://technobeans.com/2012/04/16/5-ways-of-fibonacci-in-python/

NUMBER = 15


# Example 1: Using looping technique
def fib_loop(n):
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a


print("Example 1")
print(fib_loop(NUMBER))
print()


# Example 2: Using recursion
def fib_recursion(n):
    if n == 1 or n == 2:
        return 1
    return fib_recursion(n - 1) + fib_recursion(n - 2)


print("Example 2")
print(fib_recursion(NUMBER))
print()


# Example 3: Using generators
def fib_generator():
    a, b = 0, 1
    while True:
        a, b = b, a + b
        yield a


print("Example 3")
f = fib_generator()
for _ in range(NUMBER):
    print(next(f))
print()


# Example 4: Using memoization
def memoize(fn, arg):
    memo = {}
    if arg not in memo:
        memo[arg] = fn(arg)
        return memo[arg]


# fib() as written in example 1.
print("Example 4")
fibm = memoize(fib_loop, NUMBER)
print(fibm)
print()


# Example 5: Using memoization as decorator (decorator-class)
class MemoizeClass:
    def __init__(self, func) -> None:
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


print("Example 5")
print(fib(NUMBER))
print()


# Example 6: Using memoization as decorator (decorator-function)
def memoize_func(f):
    memo = dict()

    def func(*args):
        if args not in memo:
            memo[args] = f(*args)
        return memo[args]

    return func


@memoize_func
def fib(n):
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a


print("Example 6")
print(fib(NUMBER))
print()
