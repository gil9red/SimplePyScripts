#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import fnmatch


file_name = 'README.md'

print(fnmatch.fnmatch(file_name, '*.md'))      # True
print(fnmatch.fnmatchcase(file_name, '*.md'))  # True

print(fnmatch.fnmatch(file_name, '*.MD'))      # True
print(fnmatch.fnmatchcase(file_name, '*.MD'))  # False

print(fnmatch.fnmatch(file_name, 'README.md'))      # True
print(fnmatch.fnmatchcase(file_name, 'README.md'))  # True

print(fnmatch.fnmatch(file_name, 'readme.md'))      # True
print(fnmatch.fnmatchcase(file_name, 'readme.md'))  # False
