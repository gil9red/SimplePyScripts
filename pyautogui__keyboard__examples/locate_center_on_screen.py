#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pyautogui


def locate_center_on_screen(needle_image, screenshot_image=None):
    if screenshot_image:
        rect = pyautogui.locate(needle_image, screenshot_image)
        if rect:
            return pyautogui.center(rect)

    return pyautogui.locateCenterOnScreen(needle_image)


if __name__ == "__main__":
    needle_image = "<file_name>"

    import time

    t = time.clock()
    screenshot = pyautogui.screenshot()
    pos = locate_center_on_screen(needle_image, screenshot)
    pos = locate_center_on_screen(needle_image, screenshot)
    pos = locate_center_on_screen(needle_image, screenshot)
    print(pos, time.clock() - t)

    # Without buffered image
    t = time.clock()
    pos = pyautogui.locateCenterOnScreen(needle_image)
    pos = pyautogui.locateCenterOnScreen(needle_image)
    pos = pyautogui.locateCenterOnScreen(needle_image)
    print(pos, time.clock() - t)
