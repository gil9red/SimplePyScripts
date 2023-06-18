#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import itertools


def end_zeros(num: int) -> int:
    size = 0

    for x, items in itertools.groupby(str(num)):
        if x == "0":
            size = max(size, len(list(items)))

    return size


if __name__ == "__main__":
    assert end_zeros(10979000000) == 6
    assert end_zeros(1000000) == 6
    assert end_zeros(10009) == 3
