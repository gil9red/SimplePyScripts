#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/stchris/untangle


# pip install untangle
# OR:
# pip install git+https://github.com/stchris/untangle.git
import untangle


obj = untangle.parse(
    """\
<root>
    <child name="child1"/>
    <child name="child2">Text</child>
    <child name="child3">
    This text!
    </child>
</root>
"""
)
print(
    obj.root.child
)  # [Element(name = child, attributes = {'name': 'child1'}, cdata = ), ...
print(obj.root.child[0]["name"])  # child1
print(obj.root.child[1].cdata)  # Text
print(repr(obj.root.child[2].cdata))  # '\n    This text!\n    '
# print(','.join([child['name'] for child in obj.root.child]))
print()
print()

obj = untangle.parse(
    """\
<root>
    <child name="child2">Text</child>
</root>
"""
)
print(
    obj.root.child
)  # Element <child> with attributes {'name': 'child2'}, children [] and cdata Text
print(obj.root.child["name"])  # child2
print(obj.root.child.cdata)  # Text
