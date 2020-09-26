#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re


pattern = re.compile("[a-z]+|[0-9]+", re.DEBUG)
# BRANCH
#   MAX_REPEAT 1 MAXREPEAT
#     IN
#       RANGE (97, 122)
# OR
#   MAX_REPEAT 1 MAXREPEAT
#     IN
#       RANGE (48, 57)
print()
print(type(pattern), pattern)

print('\n')

pattern = re.compile(r"\d{2,6}", re.DEBUG)
# MAX_REPEAT 2 6
#   IN
#     CATEGORY CATEGORY_DIGI
print()
print(type(pattern), pattern)
