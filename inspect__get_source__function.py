#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def foo():
    return 1

import inspect
lines = inspect.getsourcelines(foo)
print(lines)
print('Empty:', lines[0][-1].strip() == 'pass')
print()


def foo():
    pass

lines = inspect.getsourcelines(foo)
print(lines)
print('Empty:', lines[0][-1].strip() == 'pass')
