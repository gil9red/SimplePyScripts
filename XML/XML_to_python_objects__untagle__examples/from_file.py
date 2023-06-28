#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/stchris/untangle


# pip install untangle
# OR:
# pip install git+https://github.com/stchris/untangle.git
import untangle


obj = untangle.parse("data.xml")
print(
    obj.root.child
)  # [Element(name = child, attributes = {'name': 'child1'}, cdata = ), ...
print(obj.root.child[0]["name"])  # child1
print(obj.root.child[1].cdata)  # Text
print(repr(obj.root.child[2].cdata))  # '\n    This text!\n    '
