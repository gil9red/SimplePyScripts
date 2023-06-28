#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Ловим нажатие кнопки и выходим."""


import time
import sys

import win32api


while True:
    if win32api.GetAsyncKeyState(ord("Q")):
        print("Press Q")
        sys.exit()

    time.sleep(0.01)
