#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

str_to_float = lambda x: float(x.replace(",", "."))

lon = str_to_float(input())
lat = str_to_float(input())

# print("lon: {}, lat: {}".format(lon, lat), file=sys.stderr)

min_d = None
min_name = None

n = int(input())
for i in range(n):
    defib = input().split(";")

    name = defib[1]
    lon_defib = str_to_float(defib[-2])
    lat_defib = str_to_float(defib[-1])

    x = abs(lon_defib - lon) * math.cos((lon_defib + lon) / 2)
    y = abs(lat_defib - lat)

    d = math.sqrt(x * x + y * y) * 6371

    if min_d is None or d < min_d:
        min_d = d
        min_name = name

    # print("name: {}, d: {}".format(name, d), file=sys.stderr)

print(min_name)
