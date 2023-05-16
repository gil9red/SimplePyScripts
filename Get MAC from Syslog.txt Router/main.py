#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


with open("Syslog.txt") as f:
    text = f.read()

for mac in set(re.findall(r"[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}", text)):
    print(mac)
"""
51:FD:DE:2B:B6:DE
61:61:6D:3F:99:1F
03:B4:1D:40:9B:CD
AC:38:72:82:FF:C4
"""
