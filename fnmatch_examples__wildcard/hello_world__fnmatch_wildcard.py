#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.7/library/fnmatch.html#fnmatch.fnmatch


import fnmatch


file_name = "README.md"
patterns = ["*.md", "READ*", "RE*md", "RE??ME.*", "README.*", "README.md"]
template_string = "{} is {:<%s} -> {}" % len(max(patterns, key=len))

for p in patterns:
    print(template_string.format(file_name, p, fnmatch.fnmatch(file_name, p)))
# README.md is *.md      -> True
# README.md is READ*     -> True
# README.md is RE*md     -> True
# README.md is RE??ME.*  -> True
# README.md is README.*  -> True
# README.md is README.md -> True

print()

file_name = "README.txt"
for p in patterns:
    print(template_string.format(file_name, p, fnmatch.fnmatch(file_name, p)))
# README.md is *.md      -> True
# README.md is READ*     -> True
# README.md is RE*md     -> True
# README.md is RE??ME.*  -> True
# README.md is README.*  -> True
# README.md is README.md -> True
