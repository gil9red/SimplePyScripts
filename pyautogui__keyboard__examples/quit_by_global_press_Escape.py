#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import time

import keyboard


QUIT_COMBINATION = "Esc"
print('Press "{}" for QUIT'.format(QUIT_COMBINATION))


keyboard.add_hotkey(QUIT_COMBINATION, lambda: print("Quit by Escape") or os._exit(0))

i = 0
while True:
    i += 1
    print(i)

    time.sleep(1)
