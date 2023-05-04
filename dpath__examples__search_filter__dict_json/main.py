#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install dpath
import dpath.util

x = {
    "a": {
        "b": {
            "3": 2,
            "43": 30,
            "c": [],
            "d": ["red", "buggy", "bumpers"],
        }
    }
}

print(dpath.util.get(x, "a/b/d"))  # ['red', 'buggy', 'bumpers']
print(dpath.util.get(x, "a/b/d/0"))  # red
print(dpath.util.get(x, "a/b/d/1"))  # buggy
print(dpath.util.get(x, "a/b/43"))  # 30
print()

print(dpath.util.values(x, "**/43"))  # [30]
print(dpath.util.values(x, "**/d/1"))  # [buggy]
print()

print(dpath.util.search(x, "**/43"))  # {'a': {'b': {'43': 30}}}
print(list(dpath.util.search(x, "**/43", yielded=True)))  # [('a/b/43', 30)]
print()


def afilter(x):
    return str(x).isdecimal()


result = dpath.util.search(x, "**", afilter=afilter)
print(result)  # {'a': {'b': {'3': 2, '43': 30}}}

# Фильтрация через лябмды:
result = dpath.util.search(x, "**", afilter=lambda x: str(x).isdecimal())
print(result)  # {'a': {'b': {'3': 2, '43': 30}}}

result = list(dpath.util.search(x, "**", yielded=True, afilter=afilter))
print(result)  # [('a/b/3', 2), ('a/b/43', 30)]
