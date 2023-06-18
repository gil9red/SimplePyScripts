#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


def tokenize(expression):
    if not expression:
        return []

    regex = re.compile(r"\s*(=>|[-+*/%=()]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]


if __name__ == "__main__":
    print(tokenize("2 + 2 * 2"))
    print(tokenize("x = 2 + 2 * 2 + 2 % 2"))
    print(tokenize("x = y + 2"))
