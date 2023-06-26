#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pathlib


current_dir = pathlib.Path(__file__).parent
print(current_dir)

for file_name in current_dir.glob("*.py"):
    print(f"    {file_name}:\n        {file_name.read_bytes()}\n")
