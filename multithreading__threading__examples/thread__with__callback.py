#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
from threading import Thread


def go(callback_func):
    while True:
        time.sleep(2)
        callback_func(":)")


def it_callback(s):
    global status
    status = s


status = ":("

thread = Thread(target=go, args=(it_callback,))
thread.start()

while thread.is_alive():
    print(status)
    time.sleep(0.5)
