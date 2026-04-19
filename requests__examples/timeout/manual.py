#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests

TIMEOUT: float = 60

session = requests.Session()

rs = session.get("https://httpbin.org/delay/1", timeout=TIMEOUT)
print(rs)

rs = session.get("https://httpbin.org/delay/2", timeout=TIMEOUT)
print(rs)

rs = session.get("https://httpbin.org/delay/3", timeout=TIMEOUT)
print(rs)
