#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import namedtuple
from typing import NamedTuple


Point = namedtuple("Point", ["x", "y"])

# # TypeError: __new__() missing 2 required positional arguments: 'x' and 'y'
# p = Point()
# print(p)

p = Point(1, 2)
print(p)  # Point(x=1, y=2)
print(p._asdict())  # OrderedDict([('x', 1), ('y', 2)])
print()


# SOURCE: https://docs.python.org/3/library/typing.html#typing.NamedTuple
class Point(NamedTuple):
    x: int = 0
    y: int = 0


p = Point()
print(p)  # Point(x=0, y=0)

p = Point(1, 2)
print(p)  # Point(x=1, y=2)
print(p._asdict())  # OrderedDict([('x', 1), ('y', 2)])
