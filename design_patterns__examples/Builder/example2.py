#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import Any, Self


class Foo:
    def __init__(self) -> None:
        self.items = []
        self.key_by_value = dict()

    def add_item(self, value) -> Self:
        self.items.append(value)
        return self

    def add_items(self, values) -> Self:
        self.items += values
        return self

    def set_value(self, key, value) -> Self:
        self.key_by_value[key] = value
        return self

    def get_value(self, key) -> Any:
        return self.key_by_value[key]

    def __repr__(self) -> str:
        return f"Foo<items={len(self.items)}, values={len(self.key_by_value)}>"


foo = Foo().add_item(1).add_items("abc").set_value("x", 1).set_value("x[]", [1, 2, 3])

print(foo)
print(foo.items)
print(foo.key_by_value)
print(foo.get_value("x"))
print(foo.get_value("x[]"))
