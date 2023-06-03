#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import os

import keyboard
import pyautogui


QUIT_COMBINATION = "Esc"
print('Press "{}" for QUIT'.format(QUIT_COMBINATION))


keyboard.add_hotkey(QUIT_COMBINATION, lambda: print("Quit by Escape") or os._exit(0))

time.sleep(5)

i = 0
while True:
    pyautogui.press("pgdn")

    i += 1
    print(i)

    time.sleep(1)
