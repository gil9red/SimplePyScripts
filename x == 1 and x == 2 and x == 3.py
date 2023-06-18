#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


class X:
    def __eq__(self, other):
        return True


x = X()
print(x == 1 and x == 2 and x == 3)  # True
