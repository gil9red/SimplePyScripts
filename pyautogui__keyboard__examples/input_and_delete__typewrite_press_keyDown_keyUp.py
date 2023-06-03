#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://pyautogui.readthedocs.io/en/latest/keyboard.html#the-press-keydown-and-keyup-functions


# pip install pyautogui
import pyautogui


TEXT = "Hello World!"


# Input text
pyautogui.typewrite(TEXT)

# Select text
pyautogui.keyDown("shift")  # Hold down the shift key

for _ in TEXT:
    pyautogui.press("left")  # Press the left arrow key

pyautogui.keyUp("shift")  # Release the shift key

pyautogui.press("delete")
