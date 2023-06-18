#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


obj = 1

print(list(filter(lambda x: not x.startswith("_"), dir(obj))))
for i in list(filter(lambda x: not x.startswith("_"), dir(obj))):
    print(i, ":", getattr(obj, i))
print()
