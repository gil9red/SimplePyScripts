#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Only Linux

# pip install psutil
import psutil


print(psutil.sensors_temperatures())
print(psutil.sensors_fans())
print(psutil.sensors_battery())
