#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/Dark-Princ3/X-tra-Telegram/blob/aa628465dddaf06383c84914df70c89a4d4fbf15/userbot/plugins/Earth.py#L13


import time


items = "🌏🌍🌎🌎🌍🌏🌍🌎"
for i in range(48):
    print("\r" + " " * 100 + "\r", end="")
    print(items[i % len(items)], end="")
    time.sleep(0.1)
