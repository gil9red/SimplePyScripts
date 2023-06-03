#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pynput
from pynput.keyboard import Key, Listener


def on_press(key):
    print(f"{key} pressed")


def on_release(key):
    print(f"{key} release")

    if key == Key.esc:
        # Stop listener
        return False


# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
