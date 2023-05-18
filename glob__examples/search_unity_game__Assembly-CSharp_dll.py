#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import glob


pattern = r"C:\**\*Data\Managed\Assembly-CSharp.dll"

file_names = glob.glob(pattern, recursive=True)
print(len(file_names))

for file_name in file_names:
    print(file_name)
