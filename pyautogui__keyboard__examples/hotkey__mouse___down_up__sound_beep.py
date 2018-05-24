#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import pyautogui
import winsound

# pip install keyboard
import keyboard
keyboard.add_hotkey('Ctrl + 1', lambda: winsound.Beep(1000, duration=50) or pyautogui.mouseDown())
keyboard.add_hotkey('Ctrl + 2', lambda: winsound.Beep(1000, duration=50) or pyautogui.mouseUp())

keyboard.wait('Ctrl + Q')

