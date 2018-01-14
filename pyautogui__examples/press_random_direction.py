#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import pyautogui

# left up down right
directions = ['left', 'up', 'down', 'right']

import random

while True:
    direction = random.choice(directions)
    print(direction)
    pyautogui.typewrite([direction], pause=2)
