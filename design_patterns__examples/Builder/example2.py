#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


class Foo:
    def __init__(self):
        self.items = []
        self.key_by_value = dict()

    def add_item(self, value):
        self.items.append(value)
        return self

    def add_items(self, values):
        self.items += values
        return self

    def set_value(self, key, value):
        self.key_by_value[key] = value
        return self

    def get_value(self, key):
        return self.key_by_value[key]

    def __repr__(self):
        return "Foo<items={}, values={}>".format(
            len(self.items), len(self.key_by_value)
        )


foo = Foo().add_item(1).add_items("abc").set_value("x", 1).set_value("x[]", [1, 2, 3])

print(foo)
print(foo.items)
print(foo.key_by_value)
print(foo.get_value("x"))
print(foo.get_value("x[]"))
