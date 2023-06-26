#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Functors


class Foo:
    def __call__(self):
        return 1


class MySum:
    def __call__(self, *args):
        return sum(args)


class MyPow:
    def __call__(self, a, b):
        return a**b


class Bar:
    def __init__(self, start_value=0):
        self.value = start_value

    def __call__(self, *args, **kwargs):
        self.value += 1
        return self

    def __str__(self):
        return f"<Foo(value={self.value})>"


foo = Foo()
print(foo())  # 1

print(MySum()(1, 2, 3, 4))  # 10

print(MyPow()(2, 10))  # 1024

print(Bar())  # 0
print(Bar()())  # 1
print(Bar()()())  # 2
print(Bar()()()())  # 3
print(Bar()()()()())  # 4
print(Bar()()()()()())  # 5
