#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install keyboard
import keyboard

import pyautogui


keyboard.add_hotkey("Ctrl + 1", pyautogui.mouseDown)
keyboard.add_hotkey("Ctrl + 2", pyautogui.mouseUp)

keyboard.wait("Ctrl + Q")
