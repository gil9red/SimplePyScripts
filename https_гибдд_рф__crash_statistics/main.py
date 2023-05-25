#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback

# pip install simple-wait
from simple_wait import wait

from common import init_db, append_crash_statistics_db


init_db()


while True:
    try:
        append_crash_statistics_db()

        wait(hours=12)

    except Exception as e:
        print(f"ERROR: {e}:\n\n{traceback.format_exc()}")
        wait(minutes=5)
