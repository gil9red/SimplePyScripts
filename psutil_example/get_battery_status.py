#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil


battery = psutil.sensors_battery()
print(battery.percent)
