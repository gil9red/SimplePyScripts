#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.7/library/fnmatch.html#fnmatch.translate


import fnmatch
import os
import re


wildcard = "get*r.py"

items = fnmatch.filter(os.listdir("../"), wildcard)
print(*items, sep="\n")
# get_current_script_dir.py
# get_quarter.py
# get_random_hex_color.py

print()


def is_match(regex, text) -> bool:
    m = re.match(regex, text)
    return bool(m)


regex = fnmatch.translate(wildcard)
items = list(filter(lambda text: is_match(regex, text), os.listdir("../")))
print(*items, sep="\n")
# get_current_script_dir.py
# get_quarter.py
# get_random_hex_color.py
