#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import os

while True:
    os.system('fable3_backup_save.py')

    # Каждые 12 часов
    time.sleep(60 * 60 * 12)
