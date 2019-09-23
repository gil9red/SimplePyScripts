#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import traceback
from common import init_db, append_crash_statistics_db, wait


init_db()


while True:
    try:
        append_crash_statistics_db()

        wait(hours=12)

    except Exception as e:
        print('ERROR: {}:\n\n{}'.format(e, traceback.format_exc()))
        wait(minutes=5)
