#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import glob


for file_name in glob.glob("*.txt"):
    img = file_name.split(".")[0] + ".png"
    if os.path.isfile(img):
        continue

    print(f"{file_name} bad")
    os.remove(file_name)
