#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime, timedelta


utc_datetime = datetime.utcnow()

for i in range(365 + 1):
    date = utc_datetime - timedelta(days=i)
    print(date.strftime("%d/%m/%Y %H:%M:%S"))
