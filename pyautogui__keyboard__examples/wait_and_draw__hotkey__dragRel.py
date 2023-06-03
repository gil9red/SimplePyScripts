#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

import keyboard
import pyautogui


RUN_COMBINATION = "Ctrl+Shift+R"
QUIT_COMBINATION = "Esc"

print('Press "{}" for RUN'.format(RUN_COMBINATION))
print('Press "{}" for QUIT'.format(QUIT_COMBINATION))


keyboard.add_hotkey(QUIT_COMBINATION, lambda: print("Quit by Escape") or os._exit(0))
keyboard.wait(RUN_COMBINATION)

indent = 2
duration = 0.1
distance = 300

while distance > 0:
    pyautogui.dragRel(distance, 0, duration)  # move right
    distance -= indent
    pyautogui.dragRel(0, distance, duration)  # move down
    pyautogui.dragRel(-distance, 0, duration)  # move left
    distance -= indent
    pyautogui.dragRel(0, -distance, duration)  # move up
