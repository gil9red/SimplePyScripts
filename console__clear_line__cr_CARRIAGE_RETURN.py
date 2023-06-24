#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import time


for ips in (10254, 1, 10, 1, 10254, 999):
    sys.stdout.write("\r" + f"Current value [{ips}]" + " " * 100)
    sys.stdout.flush()

    time.sleep(0.5)
