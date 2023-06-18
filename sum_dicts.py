#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def sum_dicts(*dicts):
    s = dict()

    for d in dicts:
        for k, v in d.items():
            if k not in s:
                s[k] = []

            s[k].append(v)

    return s


if __name__ == "__main__":
    d1 = {"a": 2, "b": 5}
    d2 = {"a": 2, "c": 6, "z": 3}
    d3 = {"b": 2, "c": 5}
    print(sum_dicts(d1, d2, d3))  # {"a": [2, 2], "b": [5, 2], "c": [6, 5], "z": [3]}
    assert sum_dicts(d1, d2, d3) == {"a": [2, 2], "b": [5, 2], "c": [6, 5], "z": [3]}
