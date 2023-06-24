#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from io import StringIO


buffer = StringIO("dfdfdfdf\n12\n34", newline="\n")


def input(*args, **kwargs):
    return next(buffer).rstrip("\n")


text = input()
print(text)
# dfdfdfdf

a, b = int(input()), int(input())
print(a, b)
# 12 34
