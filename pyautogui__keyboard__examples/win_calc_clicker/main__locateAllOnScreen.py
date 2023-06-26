#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# OpenCv -- for performance
# pip install opencv-python
#
# pip install pyautogui
import pyautogui

from main import show_test_calc


show_test_calc()


BUTTONS = {
    "+": "buttons/add.png",
    "-": "buttons/sub.png",
    "/": "buttons/div.png",
    "*": "buttons/mul.png",
    "=": "buttons/equal.png",
}
for i in range(10):
    BUTTONS[str(i)] = f"buttons/{i}.png"

cache_pos_button = dict()

expression = "1234 * 222 + 3214 = "

for x in expression:
    if x not in BUTTONS:
        print(f'Not found: "{x}"')
        continue

    if x in cache_pos_button:
        pos_list = cache_pos_button[x]
    else:
        file_name = BUTTONS[x]
        pos_list = [
            pyautogui.center(pos) for pos in pyautogui.locateAllOnScreen(BUTTONS[x])
        ]
        if not pos_list:
            continue

        cache_pos_button[x] = pos_list

    print(x, pos_list)
    for pos in pos_list:
        pyautogui.click(pos)
