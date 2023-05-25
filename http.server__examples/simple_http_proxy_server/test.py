#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


proxies = {
    "http": "localhost:33333",
}


url = "http://httpbin.org/headers"
rs = requests.get(url, proxies=proxies)
print(rs)
print(rs.headers)
print(rs.content)
for header, value in rs.json()["headers"].items():
    if header.lower().startswith("x-my"):
        print(f"{header}: {value!r}")
"""
...
X-My-Proxy: 'hell yeah!'
"""
