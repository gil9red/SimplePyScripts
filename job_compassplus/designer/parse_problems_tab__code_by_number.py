#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import PATH_PROBLEMS_TAB, parse_text


text = PATH_PROBLEMS_TAB.read_text("utf-8")

total: int = 0
code_by_number: dict[int, int] = dict()

for p in parse_text(text):
    if p.code not in code_by_number:
        code_by_number[p.code] = 0
    code_by_number[p.code] += 1

    total += 1

print(f"Code ({len(code_by_number)}):")
for code, number in sorted(code_by_number.items(), key=lambda x: x[1], reverse=True):
    print(f"  {code}: {number}")
print(f"Total: {total}")
"""
Code (4):
  51: 4
  137: 3
  132: 2
  999: 1
Total: 10
"""
