#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT


week_number = DT.datetime.now().isocalendar()[1]
print("week_number:", week_number)
