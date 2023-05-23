#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


rs = requests.get("https://ru.stackoverflow.com/robots.txt")

for line in rs.text.splitlines():
    key, value = map(str.strip, line.split(":", maxsplit=1))
    if key == "Sitemap":
        print(value)
    # https://ru.stackoverflow.com/sitemap.xml
