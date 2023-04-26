#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests

# With threaded
for _ in range(5):
    rs = requests.get("http://127.0.0.1:6000/")
    print(rs.text)

print()

# Without threaded
for _ in range(5):
    rs = requests.get("http://127.0.0.1:6001/")
    print(rs.text)
