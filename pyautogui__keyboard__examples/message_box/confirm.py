#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pyautogui import confirm


button = confirm(text="My Text", title="My Title", buttons=["OK", "Cancel"])
print(button)
