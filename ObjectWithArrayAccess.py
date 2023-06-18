#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


class ObjectWithArrayAccess:
    def __init__(self):
        self._fields = dict()

    def __getitem__(self, item):
        return self._fields.get(item)

    def __setitem__(self, key, value):
        self._fields[key] = value

    def __len__(self):
        return len(self._fields)


if __name__ == "__main__":
    obj = ObjectWithArrayAccess()
    print(bool(obj))  # False
    obj[0] = "Hello"
    obj[1] = "world"
    print(obj._fields)  # {0: 'Hello', 1: 'world'}
    print(len(obj))  # 2
    print(bool(obj))  # True
    print(obj[0], obj[1])  # Hello world
