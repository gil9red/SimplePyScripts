#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


with open("1.txt", "a", encoding="cp1251") as f:
    f.write("фотки\n")

with open("1.txt", "a", encoding="utf-8") as f:
    f.write("фотки\n")

# OR...

with open("2.txt", "ab") as f:
    f.write("фотки\n".encode("cp1251"))

with open("2.txt", "ab") as f:
    f.write("фотки\n".encode("utf-8"))
