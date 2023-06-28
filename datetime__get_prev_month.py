#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/7153449/5909792


from datetime import date, timedelta


prev_month = date.today().replace(day=1) - timedelta(days=1)
print(prev_month)
