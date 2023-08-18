#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import time


for i in range(9 + 1):
    print(f"{i} ** 2 = {i ** 2}", file=sys.stderr)
    print(f"{i} ** 2 = {i ** 2}")
    time.sleep(0.3)

sys.exit(999)

