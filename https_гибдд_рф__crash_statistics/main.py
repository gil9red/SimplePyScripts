#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
from common import init_db, append_crash_statistics_db


init_db()


while True:
    append_crash_statistics_db()

    # Every 12 hours
    time.sleep(12 * 60 * 60)
