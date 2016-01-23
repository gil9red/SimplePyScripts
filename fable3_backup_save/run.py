#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import os

while True:
    os.system('fable3_backup_save.py')

    # Каждые 5 часов
    time.sleep(60 * 60 * 5)
