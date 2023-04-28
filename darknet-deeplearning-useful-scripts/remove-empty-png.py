#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import glob


for file_name in glob.glob("*.png"):
    img = file_name.split(".")[0] + ".txt"
    if os.path.isfile(img):
        continue

    print(f"{file_name} bad")
    os.remove(file_name)
