#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import win32clipboard
from notifications import WindowsBalloonTip


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
                title = f'Clipboard changed (len: {len(data)})'

                # Max text: 20
                text = data[:100]

                WindowsBalloonTip.balloon_tip(title, text, duration=3)

            last_data = data

    except Exception as e:
        print(e)
        pass

    finally:
        time.sleep(1)
