#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


def split_by_pair(text):
    items = []

    for i in range(0, len(text), 2):
        pair = text[i] + text[i + 1]
        items.append(pair)

    return items


def split_by_pair_1(text):
    result = [a + b for a, b in list(zip(text[::2], text[1::2]))]
    return result


def split_by_pair_2(text):
    return re.findall("..", text)


if __name__ == "__main__":
    text = "a1b2c3d4f5"

    items = split_by_pair(text)
    print(items)  # ['a1', 'b2', 'c3', 'd4', 'f5']

    items = split_by_pair_1(text)
    print(items)  # ['a1', 'b2', 'c3', 'd4', 'f5']

    items = split_by_pair_2(text)
    print(items)  # ['a1', 'b2', 'c3', 'd4', 'f5']
