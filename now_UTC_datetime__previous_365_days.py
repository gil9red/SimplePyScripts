#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT


utc_datetime = DT.datetime.utcnow()

for i in range(365 + 1):
    date = utc_datetime - DT.timedelta(days=i)
    print(date.strftime("%d/%m/%Y %H:%M:%S"))
