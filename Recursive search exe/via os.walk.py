#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os


for root, dirs, files in os.walk("C://"):
    for file in files:
        base_name, ext = os.path.splitext(file)
        if ext.lower() == ".exe":
            file_name = os.path.join(root, file)
            file_name = os.path.normpath(file_name)
            print(file_name)
