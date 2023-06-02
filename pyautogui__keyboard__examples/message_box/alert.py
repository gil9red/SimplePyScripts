#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pyautogui import alert


button = alert(text="My Text", title="My Title", button="OK")
print(button)
