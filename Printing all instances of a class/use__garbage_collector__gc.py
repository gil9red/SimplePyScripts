#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/328882/5909792


import gc


def get_instances(class_: type) -> [type]:
    return [obj for obj in gc.get_objects() if isinstance(obj, class_)]


class X:
    def __init__(self, name):
        self.name = name


x = X("x")
y = X("y")
print([r.name for r in get_instances(X)])  # ['x', 'y']

del y

print([r.name for r in get_instances(X)])  # ['x']
