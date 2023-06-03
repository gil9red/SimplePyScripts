#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pyautogui


img1 = pyautogui.screenshot()
print(img1)

img2 = pyautogui.screenshot("my_screenshot.png")  # save file
print(img2)
