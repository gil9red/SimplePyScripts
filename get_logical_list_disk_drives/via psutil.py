#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import psutil
for disk in psutil.disk_partitions():
    print(disk)
