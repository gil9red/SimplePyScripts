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

import pyautogui

cache_pos_button = dict()

expression = '3,14159265358979323846264338327950288419716939937510582097494459230781640628620' \
             '8998628034825342117067982148086513282306647093844609550582231725359408128481117'

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
