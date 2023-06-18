#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import time

import win32api
import win32event
import winerror


# Prevent multiple instances
mutex = win32event.CreateMutex(None, 1, "MY_MUTEX_PYTHON")
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    print("Already running!")
    mutex = None
    sys.exit(0)

while True:
    time.sleep(99999)
