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

expression = '1234567890 * 2 = '

for x in expression:
    if x not in BUTTONS:
        print('Not found: "{}"'.format(x))
        continue

    file_name = BUTTONS[x]
    pos = pyautogui.locateCenterOnScreen(file_name, grayscale=True)
    print(x, pos)
    pyautogui.click(pos)
