#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import glob


for file_name in glob.iglob("C://**/*.exe", recursive=True):
    print(file_name)
