#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


BUTTONS = {
    '+': 'buttons/add.png',
    '-': 'buttons/sub.png',
    '/': 'buttons/div.png',
    '*': 'buttons/mul.png',
    '=': 'buttons/equal.png',
}
for i in range(10):
    BUTTONS[str(i)] = 'buttons/{}.png'.format(i)

cache_pos_button = dict()

import pyautogui

expression = '1234567890 * 2 = '

for x in expression:
    if x not in BUTTONS:
        print('Not found: "{}"'.format(x))
        continue

    if x in cache_pos_button:
        pos = cache_pos_button[x]
    else:
        file_name = BUTTONS[x]
        pos = pyautogui.locateCenterOnScreen(file_name)
        if not pos:
            continue

        cache_pos_button[x] = pos

    print(x, pos)
    pyautogui.click(pos)
