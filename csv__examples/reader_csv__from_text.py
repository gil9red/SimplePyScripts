#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import csv
from io import StringIO


text = """\
id;name;address;zip
1;vasya;moscow;11111
2;oleg;sochi;22222
"""

# Variant 1
csv_reader = csv.reader(text.splitlines(), delimiter=";")
for row in csv_reader:
    print(row)

print()

# Variant 2
csv_reader = csv.reader(StringIO(text), delimiter=";")
for row in csv_reader:
    print(row)

print()
