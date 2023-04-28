#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import glob
import sys
from os.path import dirname


cur_dir = dirname(sys.argv[0])


with open("train.txt", "w") as f:
    for file_name in glob.glob(f"{cur_dir}/*.png"):
        f.write(f"{file_name}\n")
