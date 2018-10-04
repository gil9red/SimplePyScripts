#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import traceback
from common import init_db, append_crash_statistics_db


init_db()


while True:
    try:
        append_crash_statistics_db()

        # Every 12 hours
        time.sleep(12 * 60 * 60)

    except Exception as e:
        print('ERROR: {}:\n\n{}'.format(e, traceback.format_exc()))
        print('Wait 5 minutes.')

        time.sleep(60 * 5)
