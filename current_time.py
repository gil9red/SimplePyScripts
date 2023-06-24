#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://docs.python.org/3.4/library/datetime.html
# https://docs.python.org/3.4/library/time.html


import datetime as dt
import time


while True:
    cur_time = dt.datetime.now().time()
    print("Current time is: %s" % cur_time.strftime("%H:%M:%S"), end="\r")

    # every 0.5 second (500 millisecond)
    time.sleep(0.5)
