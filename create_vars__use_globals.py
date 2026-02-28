#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


globals()["abc"] = 123
print(abc)  # 123

for key, value in {"a": 1, "b": 2}.items():
    globals()[key] = value

print(a)  # 1
print(b)  # 2
print()


number = 0


def counter() -> None:
    # If not exists global <number>
    # if 'number' not in globals():
    #     globals()['number'] = 0

    globals()["number"] += 1


counter()

print(number)  # 1

counter()
counter()
print(number)  # 3
