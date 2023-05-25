#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys

# Import https://github.com/gil9red/SimplePyScripts/blob/8fa9b9c23d10b5ee7ff0161da997b463f7a861bf/wait/wait.py
sys.path.append('../wait')
from wait import wait

from common import init_db, append_crash_statistics_db


init_db()


while True:
    try:
        append_crash_statistics_db()

        wait(hours=12)

    except Exception as e:
        print(f"ERROR: {e}:\n\n{traceback.format_exc()}")
        wait(minutes=5)
