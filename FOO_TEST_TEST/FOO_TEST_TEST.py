#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


# TODO: Global key hook Escape -- close script

import time
import pyautogui

time.sleep(5)

# distance = 400
# while distance > 0:
#     pyautogui.dragRel(distance, 0, duration=0.5)   # move right
#     distance -= 5
#     pyautogui.dragRel(0, distance, duration=0.5)   # move down
#     pyautogui.dragRel(-distance, 0, duration=0.5)  # move left
#     distance -= 5
#     pyautogui.dragRel(0, -distance, duration=0.5)  # move up

distance = 300
while distance > 0:
    pyautogui.dragRel(distance, 0)   # move right
    distance -= 2
    pyautogui.dragRel(0, distance)   # move down
    pyautogui.dragRel(-distance, 0)  # move left
    distance -= 2
    pyautogui.dragRel(0, -distance)  # move up

