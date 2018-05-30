#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def foo():
    return 1


class Foo:
    def __call__(self):
        return 1


import inspect
print(inspect.isfunction(lambda: 1))  # True
print(inspect.isfunction(foo))  # True

# Functor
print(inspect.isfunction(Foo()))  # False
