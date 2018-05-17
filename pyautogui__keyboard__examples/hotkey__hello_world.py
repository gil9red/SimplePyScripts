#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def foo():
    print('World')


# pip install keyboard
import keyboard
keyboard.add_hotkey('Ctrl + 1', lambda: print('Hello'))
keyboard.add_hotkey('Ctrl + 2', foo)
keyboard.wait('Ctrl + Q')
