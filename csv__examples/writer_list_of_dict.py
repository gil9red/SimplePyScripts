#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/csv.html#csv.DictWriter
# SOURCE: https://stackoverflow.com/a/3087011/5909792


import csv


items = [
    {"name": "bob", "age": 25, "weight": 200},
    {"name": "jim", "age": 31, "weight": 180},
]

keys = items[0].keys()
with open("people.csv", "w", encoding="utf-8", newline="") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(items)
