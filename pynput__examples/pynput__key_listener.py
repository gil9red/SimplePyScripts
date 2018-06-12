#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def on_press(key):
    print('on_press', str(key), key, type(key))


def on_release(key):
    print('on_release', str(key), key, type(key))


# pip install pynput
from pynput import keyboard
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
