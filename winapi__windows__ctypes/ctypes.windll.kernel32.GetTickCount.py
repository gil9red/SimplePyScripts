#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import ctypes
GetTickCount = ctypes.windll.kernel32.GetTickCount
t = GetTickCount()

import time
time.sleep(1)

print(f'Elapsed: {GetTickCount() - t} ms')
