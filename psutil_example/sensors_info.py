#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install psutil

# Only Linux:
import psutil
print(psutil.sensors_temperatures())
print(psutil.sensors_fans())
print(psutil.sensors_battery())

