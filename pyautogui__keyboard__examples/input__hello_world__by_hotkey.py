#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install keyboard
import keyboard


keyboard.add_hotkey(
    "Shift + Home",
    lambda: keyboard.write("Hello") or keyboard.write(" world!", delay=0.3),
)

# Block forever.
keyboard.wait()
