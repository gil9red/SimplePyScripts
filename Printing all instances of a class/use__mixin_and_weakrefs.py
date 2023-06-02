#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/328882/5909792


from collections import defaultdict
import weakref


class KeepRefs:
    __refs__ = defaultdict(list)

    def __init__(self):
        self.__refs__[self.__class__].append(weakref.ref(self))

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst


class X(KeepRefs):
    def __init__(self, name):
        super().__init__()
        self.name = name


x = X("x")
y = X("y")
print([r.name for r in X.get_instances()])  # ['x', 'y']

del y

print([r.name for r in X.get_instances()])  # ['x']
