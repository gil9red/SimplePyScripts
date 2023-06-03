#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install keyboard
import keyboard

import pyautogui

import winsound


keyboard.add_hotkey(
    "Ctrl + 1", lambda: pyautogui.mouseDown() or winsound.Beep(1000, duration=50)
)
keyboard.add_hotkey(
    "Ctrl + 2", lambda: pyautogui.mouseUp() or winsound.Beep(1000, duration=50)
)

keyboard.wait("Ctrl + Q")
