#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def nearest(lst, target):
    return min(lst, key=lambda x: abs(x - target))


if __name__ == "__main__":
    l = [5, 78, 45, 12, 56, 9999]
    print(nearest(l, 52))  # 56
    print(nearest(l, 50))  # 45
