#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import itertools


DIFF_SECS = 60

items = [
    [DT.datetime.now(), DT.datetime.now() + DT.timedelta(hours=1), DT.datetime.now() + DT.timedelta(seconds=30)],
    [DT.datetime.now(), DT.datetime.now() + DT.timedelta(hours=1)],
    [DT.datetime.now()],
]

for x in items:
    found = any(abs((dt1 - dt2).total_seconds()) <= DIFF_SECS for dt1, dt2 in itertools.combinations(x, 2))
    if found:
        print(x)
