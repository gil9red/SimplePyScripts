#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import win32clipboard

last_data = None

while True:
    try:
        # Get clipboard data
        win32clipboard.OpenClipboard()
        try:
            data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        finally:
            win32clipboard.CloseClipboard()

        if data != last_data:
            # First changed without notification
            if last_data is not None:
                print("Clipboard changed: " + data)

            last_data = data

    except:
        pass

    finally:
        time.sleep(1)
