#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import inspect



def foo():
    return 1


class Foo:
    def __call__(self):
        return 1


print(inspect.isroutine(lambda: 1))  # True
print(inspect.isroutine(foo))  # True
print()

# Functor
foo = Foo()
print(inspect.isroutine(foo))  # False
print(hasattr(foo, "__call__"))  # True
print(callable(foo))  # True
print()

import math

print(inspect.isroutine(math.sin))  # True
print(inspect.isroutine(print))  # True
