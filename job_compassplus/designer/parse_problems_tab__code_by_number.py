#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from pathlib import Path


text = (Path(__file__).parent / "problems_tab.txt").read_text("utf-8")

total = 0
code_by_number: dict[str, int] = dict()
for line in text.strip().splitlines():
    if not line.startswith("*"):
        continue

    m = re.search(r"\* \[\w+\] (\d+) - ", line)
    code: str = m.group(1) if m else "<unknown>"

    if code not in code_by_number:
        code_by_number[code] = 0
    code_by_number[code] += 1

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
