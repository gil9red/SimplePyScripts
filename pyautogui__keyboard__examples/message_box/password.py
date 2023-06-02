#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pyautogui import password


result = password(text="My Text", title="My Title", default="Default Text", mask="*")
print(result)

result = password(text="My Text", title="My Title", default="Default Text", mask="?")
print(result)
