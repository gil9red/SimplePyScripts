#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# TODO: https://docs.python.org/3/library/collections.html#collections.namedtuple_example
# Basic example


from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])
p = Point(11, y=22)  # instantiate with positional or keyword arguments
print(p[0] + p[1])   # indexable like the plain tuple (11, 22)
x, y = p             # unpack like a regular tuple
print(x, y)
print(p.x + p.y)     # fields also accessible by name
print(p)             # readable __repr__ with a name=value style
print()

XYZPoint = namedtuple("XYZPoint", ["x", "y", "z"])
xyz = XYZPoint(2, 2, z=5)
print(xyz)
print("z:", xyz.z)
print("Points: x: {x}, y: {y}, z: {z}".format(**xyz._asdict()))
