#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install keyboard
import keyboard


keyboard.add_hotkey("Win + PageDown", lambda: keyboard.send("Alt + Space + N"))

# Block forever.
keyboard.wait()
