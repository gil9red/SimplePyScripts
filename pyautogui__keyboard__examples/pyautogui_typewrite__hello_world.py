#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pyautogui
import pyautogui


# Prints out "Hello world!" instantly
pyautogui.typewrite("Hello world!")

pyautogui.press("enter")

# Prints out "Hello world!" with a quarter second delay after each character
pyautogui.typewrite("Hello world!", interval=0.25)
