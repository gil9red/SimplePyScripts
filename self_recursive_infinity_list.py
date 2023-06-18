#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


lst = [1, 2]
lst.insert(0, lst)
print(lst)  # [[...], 1, 2]
print(lst[0][0][0][2])  # 2
