#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


rs = requests.get("https://pomber.github.io/covid19/timeseries.json")
print(f"{int(rs.headers.get('Content-Length')) / 1024 / 1024:.2f} MB")

data = rs.json()
print(data)

for x in data["Russia"]:
    print(x)
