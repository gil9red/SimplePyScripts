#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import fnmatch

file_name = 'README.md'
patterns = ['*.md', 'READ*', 'RE*md', 'RE??ME.*']
template_string = '{} is {:<%s} -> {}' % len(max(patterns, key=len))

for p in patterns:
    print(template_string.format(file_name, p, fnmatch.fnmatch(file_name, p)))
# README.md is *.md     -> True
# README.md is READ*    -> True
# README.md is RE*md    -> True
# README.md is RE??ME.* -> True

print()

file_name = 'README.txt'
for p in patterns:
    print(template_string.format(file_name, p, fnmatch.fnmatch(file_name, p)))
# README.txt is *.md     -> False
# README.txt is READ*    -> True
# README.txt is RE*md    -> False
# README.txt is RE??ME.* -> True
