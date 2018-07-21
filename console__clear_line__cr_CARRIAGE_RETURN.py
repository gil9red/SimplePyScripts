#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time

for ips in (10254, 1, 10, 1, 10254, 999):
    print(f'Current value [{ips}]', end='\r\n')

    time.sleep(0.5)
