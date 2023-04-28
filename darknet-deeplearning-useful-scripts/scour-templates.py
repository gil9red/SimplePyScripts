#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import glob
from os.path import basename


print("reading")
templates = [
    int(basename(f).split(".")[0])
    for f in glob.glob("*.png")
]

print("sorting")
templates.sort()

index = templates[0]

print("renaming")
for i in templates:
    try:
        if i != index:
            os.rename(f"{i}.txt", f"{index}.txt")
            os.rename(f"{i}.png", f"{index}.png")
    except OSError as err:
        print(f"bad index {i}")
        raise err

    index += 1
