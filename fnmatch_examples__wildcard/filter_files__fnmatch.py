#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import fnmatch
import os


for file in os.listdir('../'):
    if fnmatch.fnmatch(file, 'get*r.py'):
        print(file)
# get_current_script_dir.py
# get_quarter.py
# get_random_hex_color.py
