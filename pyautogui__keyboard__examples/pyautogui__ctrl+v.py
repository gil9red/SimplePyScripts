#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install pyautogui
import pyautogui

# Variant 1
pyautogui.hotkey("Ctrl", "V")

# Variant 2
pyautogui.keyDown('Ctrl')
pyautogui.press('V')
pyautogui.keyUp('Ctrl')
