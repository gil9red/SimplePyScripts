#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime, timedelta, timezone


utc_datetime = datetime.now(timezone.utc)

for i in range(365 + 1):
    date = utc_datetime - timedelta(days=i)
    print(date.strftime("%d/%m/%Y %H:%M:%S"))
