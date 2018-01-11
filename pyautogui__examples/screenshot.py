#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import pyautogui
im1 = pyautogui.screenshot()
print(im1)

im2 = pyautogui.screenshot('my_screenshot.png')  # save file
print(im2)
