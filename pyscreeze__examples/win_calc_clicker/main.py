#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import win32api
import win32con

from pathlib import Path

# pip install pyscreeze
import pyscreeze


DIR = Path(__file__).parent.resolve()
DIR_BUTTONS = DIR / 'buttons'


def click(x, y, sleep_secs: float = 0.01):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    time.sleep(sleep_secs)


BUTTON_BY_POSITION = dict()


def init_button_positions(grayscale: bool = True):
    BUTTON_BY_POSITION.clear()

    for path in DIR_BUTTONS.glob('*.png'):
        button = path.stem

        position = pyscreeze.locateCenterOnScreen(str(path), grayscale=grayscale)
        if not position:
            print(f'Position of button {button!r} not found!')
            continue

        BUTTON_BY_POSITION[button] = position


def go(expression: str):
    init_button_positions()

    for button in expression:
        if not button.strip():
            continue

        if button not in BUTTON_BY_POSITION:
            print(f'Unknown button {button!r}!')
            continue

        x, y = BUTTON_BY_POSITION[button]
        print(f'Click on {button!r} at {x}x{y}')

        click(x, y)


def show_test_calc():
    import os
    os.startfile('calc.exe')

    time.sleep(1)


if __name__ == '__main__':
    show_test_calc()

    expression = '1234 + 222 + 3214 + 1111 + 1234567890 + 222 = '
    go(expression)
