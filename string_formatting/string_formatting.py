#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


class Foo:
    def __init__(self, a, b):
        self.a = a
        self.b = b


print("{one} * {one} {two}".format(one="45", two="Bugaga"))
# 45 * 45 Bugaga

print("{foo.a}, {foo.b}".format(foo=Foo("a", "b")))
# a, b

print(
    "{foo_list[0].a}, {foo_list[1].b}".format(
        foo_list=[
            Foo("a1", "b1"),
            Foo("a2", "b2"),
        ]
    )
)
# a1, b2
