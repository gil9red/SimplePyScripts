#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install keyboard
import keyboard


def foo() -> None:
    print("World")


keyboard.add_hotkey("Ctrl + 1", lambda: print("Hello"))
keyboard.add_hotkey("Ctrl + 2", foo)

keyboard.wait("Ctrl + Q")
