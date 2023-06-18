#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


class A:
    pass


a = A()
print(A.__name__)  # A
print(a.__class__.__name__)  # A


class B:
    def __init__(self):
        print(self.__class__.__name__)  # B


B()
