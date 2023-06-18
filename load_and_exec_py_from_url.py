#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.request import urlopen


url = "https://raw.githubusercontent.com/gil9red/SimplePyScripts/c4ef2f1636f7d75b87807e858ea1eea6116df773/print_triangle.py"

with urlopen(url) as f:
    exec(f.read())
