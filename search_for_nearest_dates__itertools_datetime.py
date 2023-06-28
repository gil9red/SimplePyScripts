#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import itertools
from datetime import datetime, timedelta


DIFF_SECS = 60

items = [
    [datetime.now(), datetime.now() + timedelta(hours=1), datetime.now() + timedelta(seconds=30)],
    [datetime.now(), datetime.now() + timedelta(hours=1)],
    [datetime.now()],
]

for x in items:
    found = any(
        abs((dt1 - dt2).total_seconds()) <= DIFF_SECS
        for dt1, dt2 in itertools.combinations(x, 2)
    )
    if found:
        print(x)
