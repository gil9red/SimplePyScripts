#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


rs = requests.get("http://127.0.0.1:8080/api/v2/torrents/info")
print(rs)
print(rs.text)
