#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.7/library/fnmatch.html#fnmatch.filter


import fnmatch
import os


items = fnmatch.filter(os.listdir("../"), "get*r.py")
print(*items, sep="\n")
# get_current_script_dir.py
# get_quarter.py
# get_random_hex_color.py
