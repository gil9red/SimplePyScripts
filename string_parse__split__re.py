#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


text = """\
Пушкин 1799-1837
Лермонтов 1814-1841
"""


for name, start, end in re.findall(r"(\w+) (\d+)-(\d+)", text):
    print(f"{name}, {int(end) - int(start)} лет")

print()

for line in text.splitlines():
    name, age = line.split()
    start, end = map(int, age.split("-"))

    print(f"{name}, {end - start} лет")
