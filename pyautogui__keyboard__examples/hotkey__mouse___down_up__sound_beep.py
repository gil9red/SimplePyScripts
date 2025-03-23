#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import winsound

# pip install keyboard==0.13.5
import keyboard

# pip install pyautogui==0.9.54
import pyautogui


def beep():
    winsound.Beep(1000, duration=50)


keyboard.add_hotkey(
    "Ctrl + 1", lambda: pyautogui.mouseDown() or beep()
)
keyboard.add_hotkey(
    "Ctrl + 2", lambda: pyautogui.mouseUp() or beep()
)

keyboard.wait("Ctrl + Q")
