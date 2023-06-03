#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import time

from pathlib import Path

import pyautogui


DIR = Path(__file__).resolve().parent

DIR_SCREENSHOTS = DIR / "screenshots"
DIR_SCREENSHOTS.mkdir(parents=True, exist_ok=True)


while True:
    file_name = str(DIR_SCREENSHOTS / f"{DT.datetime.now():%Y-%m-%d_%H%M%S.%f}.png")
    print(file_name)

    pyautogui.screenshot(file_name)  # Save file

    time.sleep(0.5)
