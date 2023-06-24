#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/7153449/5909792


import datetime as DT


prev_month = DT.date.today().replace(day=1) - DT.timedelta(days=1)
print(prev_month)
