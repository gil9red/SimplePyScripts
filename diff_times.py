#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT


check_hours, check_minutes = 16, 29

dt = DT.datetime.now()
check_dt = dt.replace(hour=check_hours, minute=check_minutes)

if dt > check_dt:
    print(dt - check_dt)
else:
    print(check_dt - dt)

# 0:38:00
