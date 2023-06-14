#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path


for file_name in Path("C://").rglob("*.exe"):
    print(file_name)
