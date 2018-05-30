#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Functors


class Foo:
    def __call__(self):
        return 1


class MySum:
    def __call__(self, *args):
        return sum(args)


class MyPow:
    def __call__(self, a, b):
        return a ** b


foo = Foo()
print(foo())  # 1

print(MySum()(1, 2, 3, 4))  # 10

print(MyPow()(2, 10))  # 1024
