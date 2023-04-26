#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from string import ascii_lowercase


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l = int(input())
h = int(input())
t = input()

print(l, file=sys.stderr)
print(h, file=sys.stderr)
print(t, file=sys.stderr)
print("\n", file=sys.stderr)

ascii_rows = [input() for i in range(h)]
print("\n".join(ascii_rows), file=sys.stderr)
print("\n", file=sys.stderr)

letter_list = list(ascii_lowercase) + ["?"]

result_rows = list()

for row in ascii_rows:
    new_row = ""
    for c in t.lower():
        if c not in letter_list:
            c = "?"

        index = letter_list.index(c)

        pos = index * l
        new_row += row[pos : pos + l]

    result_rows.append(new_row)

print("\n".join(result_rows))
