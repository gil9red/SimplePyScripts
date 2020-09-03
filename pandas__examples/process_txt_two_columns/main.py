#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import pandas as pd

df = pd.read_csv("001.txt", sep=":", header=None, dtype="str")

for index, row in df.iterrows():
    row[1] = ''.join('1' if x == '0' else '0' for x in row[1].strip())

df.to_csv("002.txt", index=None, header=None, sep=":")
