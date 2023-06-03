#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
import pyautogui


# left up down right
directions = ["left", "up", "down", "right"]

while True:
    direction = random.choice(directions)
    print(direction)
    pyautogui.typewrite([direction], pause=2)
